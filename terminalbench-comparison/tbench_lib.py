import requests
import re
import json
import sys
from urllib.parse import quote

def fetch_leaderboard_data(url):
    """
    Fetches the leaderboard page and extracts the JSON data containing task performance.
    Returns a dict with:
      - 'results': {taskName: {avgResolutionRate: float, successCount: int, nTrials: int}}
      - 'metadata': {agentName: str, agentVersion: str, modelName: str}
    """
    # print(f"Fetching leaderboard data from: {url}", file=sys.stderr)
    try:
        response = requests.get(url)
        response.raise_for_status()
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

    # Try finding the full JSON array first if the regex failed due to complexity
    # Look for a large array of objects with taskName
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
        # Fallback regex extraction for tasks
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
        print(f"Could not extract data from {url}", file=sys.stderr)
        return None

    return {'results': results, 'metadata': metadata}

def fetch_registry_metadata():
    """
    Fetches the registry page and extracts task metadata (Category, Difficulty).
    Returns a dict: {taskName: {'category': str, 'difficulty': str}}
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
    Returns: list of dicts {rank, name, url, accuracy}
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

    # Extract the main JSON blob containing the list
    # Look for [{"agent":...}]
    # We use a pattern that captures the agentName and modelNames which are crucial for URL construction

    # The JSON usually comes in a big escaped string in __next_f.push
    # We can try to regex for the specific objects

    # Pattern to find objects with agentName, agentVersion, modelNames
    # We'll just scan for the full JSON array if possible

    # Search for the start of the list
    match = re.search(r'\\?\"agentName\\?\":', html)
    if not match:
        print("Could not find agent list in leaderboard HTML", file=sys.stderr)
        return []

    # Use a simpler regex to extract individual entries one by one
    # {"agent":"...","agentName":"...","agentVersion":"...","modelNames":["..."]...}

    # This regex is a bit loose but aims to capture the relevant fields
    # It assumes keys are close to each other

    # Actually, let's try to grab the whole JSON array string again
    # It's likely in `self.__next_f.push([..., "[{...}]"])`

    # Let's try to extract all objects that have 'agentName'
    # We use a regex that captures the content between { and } that contains "agentName"

    # Better: find the specific JSON list structure we saw in the curl output
    # [{"agent":...}]

    json_list_match = re.search(r'(\[\{\\?"agent\\?":.*?\}\])', html)
    if json_list_match:
        json_str = json_list_match.group(1)
        if '\\"' in json_str:
            json_str = json_str.replace('\\"', '"')

        try:
            data = json.loads(json_str)
            # data should be the list of agents

            # Sort by accuracy descending just in case, though usually pre-sorted
            # accuracy field exists

            # Filter valid entries
            valid_data = [d for d in data if isinstance(d, dict) and 'agentName' in d]

            # Sort by accuracy
            valid_data.sort(key=lambda x: x.get('accuracy', 0), reverse=True)

            for i, item in enumerate(valid_data):
                agent_name = item.get('agentName')
                agent_version = item.get('agentVersion', 'unknown')
                model_names = item.get('modelNames', [])
                accuracy = item.get('accuracy', 0)

                if not model_names:
                    continue

                model_name = model_names[0]

                # Construct URL
                # https://www.tbench.ai/leaderboard/terminal-bench/2.0/{agentName}/{agentVersion}/{modelName}
                # Must encode components

                safe_agent = quote(agent_name)
                safe_version = quote(agent_version)
                safe_model = quote(model_name)

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
