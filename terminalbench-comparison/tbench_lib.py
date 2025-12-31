import requests
import re
import json
import sys
from urllib.parse import quote
import sqlite3
import datetime
import os

# Determine DB path relative to this library file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tbench.db")

def init_db():
    """Initializes the SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            agent_name TEXT,
            agent_version TEXT,
            model_name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER,
            task_name TEXT,
            resolution_rate REAL,
            success_count INTEGER,
            n_trials INTEGER,
            category TEXT,
            difficulty TEXT,
            FOREIGN KEY(run_id) REFERENCES runs(id)
        )
    ''')

    conn.commit()
    conn.close()

def save_run_to_db(url, data):
    """Saves a run and its tasks to the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    meta = data['metadata']
    results = data['results']
    registry = fetch_registry_metadata() # Fetch fresh or use cached if passed

    try:
        # Check if exists
        c.execute("SELECT id FROM runs WHERE url = ?", (url,))
        row = c.fetchone()

        if row:
            run_id = row[0]
            # Update meta
            c.execute("""
                UPDATE runs
                SET agent_name=?, agent_version=?, model_name=?, timestamp=CURRENT_TIMESTAMP
                WHERE id=?
            """, (meta['agentName'], meta['agentVersion'], meta['modelName'], run_id))
            # Delete old tasks to replace
            c.execute("DELETE FROM tasks WHERE run_id=?", (run_id,))
        else:
            c.execute("""
                INSERT INTO runs (url, agent_name, agent_version, model_name)
                VALUES (?, ?, ?, ?)
            """, (url, meta['agentName'], meta['agentVersion'], meta['modelName']))
            run_id = c.lastrowid

        # Insert tasks
        task_rows = []
        for task_name, res in results.items():
            task_meta = registry.get(task_name, {'category': 'Unknown', 'difficulty': 'Unknown'})
            task_rows.append((
                run_id,
                task_name,
                res['avgResolutionRate'],
                res['successCount'],
                res['nTrials'],
                task_meta['category'],
                task_meta['difficulty']
            ))

        c.executemany("""
            INSERT INTO tasks (run_id, task_name, resolution_rate, success_count, n_trials, category, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, task_rows)

        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving to DB: {e}", file=sys.stderr)
        return False
    finally:
        conn.close()

def get_all_runs_from_db():
    """Retrieves all runs and their task data from the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    runs = {}

    try:
        c.execute("SELECT * FROM runs ORDER BY timestamp DESC")
        run_rows = c.fetchall()

        for run in run_rows:
            run_id = run['id']
            # Reconstruct the structure used by dashboard
            # Key: "Agent / Model"
            run_key = f"{run['agent_name']} / {run['model_name']}"

            c.execute("SELECT * FROM tasks WHERE run_id=?", (run_id,))
            task_rows = c.fetchall()

            results = {}
            for task in task_rows:
                results[task['task_name']] = {
                    'avgResolutionRate': task['resolution_rate'],
                    'successCount': task['success_count'],
                    'nTrials': task['n_trials']
                }

            runs[run_key] = {
                'metadata': {
                    'agentName': run['agent_name'],
                    'agentVersion': run['agent_version'],
                    'modelName': run['model_name']
                },
                'results': results,
                'db_url': run['url'] # Keep track of source URL
            }

    except Exception as e:
        print(f"Error reading DB: {e}", file=sys.stderr)
    finally:
        conn.close()

    return runs

def fetch_leaderboard_data(url):
    """
    Fetches the leaderboard page and extracts the JSON data containing task performance.
    """
    try:
        response = requests.get(url)
        # response.raise_for_status() # Don't raise, handle 404 gracefully
        if response.status_code != 200:
            print(f"Error fetching {url}: Status {response.status_code}", file=sys.stderr)
            return None
        html = response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

    results = {}
    metadata = {
        'agentName': 'Unknown',
        'agentVersion': 'Unknown',
        'modelName': 'Unknown'
    }

    match = re.search(r'(\[\{.*?"taskName".*?\}\])', html)

    if match:
        json_str = match.group(1)
        if '\\"' in json_str:
            json_str = json_str.replace('\\"', '"')

        try:
            data = json.loads(json_str)

            def extract_items(obj):
                items = []
                if isinstance(obj, list):
                    for x in obj:
                        items.extend(extract_items(x))
                elif isinstance(obj, dict):
                    items.append(obj)
                return items

            flat_items = extract_items(data)

            for item in flat_items:
                if 'taskName' in item:
                    results[item['taskName']] = {
                        'avgResolutionRate': float(item.get('avgResolutionRate', 0)),
                        'successCount': int(item.get('successCount', 0)),
                        'nTrials': int(item.get('nTrials', 0))
                    }

                if 'agentName' in item:
                    metadata['agentName'] = item['agentName']
                if 'agentVersion' in item:
                    metadata['agentVersion'] = item['agentVersion']
                if 'models' in item:
                    metadata['modelName'] = item['models']

        except Exception as e:
            print(f"Error parsing JSON: {e}", file=sys.stderr)
    else:
        pattern = r'\\?"taskName\\?":\s*\\?"([^"\\]+)\\?",.*?\\?"avgResolutionRate\\?":\s*([\d\.]+),.*?\\?"successCount\\?":\s*(\d+)'
        matches = re.findall(pattern, html)
        for task_name, rate, success_count in matches:
             results[task_name] = {
                'avgResolutionRate': float(rate),
                'successCount': int(success_count),
                'nTrials': 5
            }

        agent_match = re.search(r'\\?"agentName\\?":\s*\\?"([^"\\]+)\\?"', html)
        if agent_match:
            metadata['agentName'] = agent_match.group(1)

        version_match = re.search(r'\\?"agentVersion\\?":\s*\\?"([^"\\]+)\\?"', html)
        if version_match:
            metadata['agentVersion'] = version_match.group(1)

        model_match = re.search(r'\\?"models\\?":\s*\\?"([^"\\]+)\\?"', html)
        if model_match:
            metadata['modelName'] = model_match.group(1)

    if not results:
        # print(f"Could not extract data from {url}", file=sys.stderr)
        return None

    return {'results': results, 'metadata': metadata}

def fetch_registry_metadata():
    """
    Fetches the registry page and extracts task metadata (Category, Difficulty).
    """
    url = "https://www.tbench.ai/registry/terminal-bench/2.0"
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print(f"Error fetching registry: {e}", file=sys.stderr)
        return {}

    metadata = {}

    parts = html.split('href="/registry/terminal-bench/2.0/')

    for part in parts[1:]:
        task_name = part.split('"')[0]
        snippet = part[:4000]

        badges = re.findall(r'<span data-slot="badge"[^>]*>([^<]+)</span>', snippet)

        category = "Unknown"
        difficulty = "Unknown"

        known_difficulties = {'easy', 'medium', 'hard'}
        cats = []

        for b in badges:
            b_lower = b.lower()
            if b_lower in known_difficulties:
                difficulty = b
            elif b_lower != "github":
                cats.append(b)

        if cats:
            category = ", ".join(cats)

        metadata[task_name] = {
            'category': category,
            'difficulty': difficulty
        }

    return metadata

def fetch_leaderboard_list():
    """
    Fetches the main leaderboard page and returns a list of top models with their details.
    """
    url = "https://www.tbench.ai/leaderboard/terminal-bench/2.0"
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print(f"Error fetching leaderboard list: {e}", file=sys.stderr)
        return []

    entries = []

    json_list_match = re.search(r'(\[\{\\?"agent\\?":.*?\}\])', html)
    if json_list_match:
        json_str = json_list_match.group(1)
        if '\\"' in json_str:
            json_str = json_str.replace('\\"', '"')

        try:
            data = json.loads(json_str)
            valid_data = [d for d in data if isinstance(d, dict) and 'agentName' in d]
            valid_data.sort(key=lambda x: x.get('accuracy', 0), reverse=True)

            for i, item in enumerate(valid_data):
                agent_name = item.get('agentName')
                agent_version = item.get('agentVersion', 'unknown')
                model_names = item.get('modelNames', [])
                model_providers = item.get('modelProviders', [])
                accuracy = item.get('accuracy', 0)

                if not model_names:
                    continue

                model_name = model_names[0]

                final_model_str = model_name
                if '@' not in model_name and model_providers:
                    provider = model_providers[0]
                    final_model_str = f"{model_name}@{provider}"

                safe_agent = quote(agent_name)
                safe_version = quote(agent_version)
                safe_model = quote(final_model_str)

                full_url = f"https://www.tbench.ai/leaderboard/terminal-bench/2.0/{safe_agent}/{safe_version}/{safe_model}"

                entries.append({
                    'rank': i + 1,
                    'name': f"{agent_name} / {model_name}",
                    'url': full_url,
                    'accuracy': accuracy
                })

        except Exception as e:
            print(f"Error parsing leaderboard JSON: {e}", file=sys.stderr)

    return entries
