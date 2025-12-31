import argparse
import requests
import re
import json
import sys

def fetch_leaderboard_data(url):
    """
    Fetches the leaderboard page and extracts the JSON data containing task performance.
    Returns a dict: {taskName: {avgResolutionRate: float, successCount: int, nTrials: int}}
    """
    print(f"Fetching leaderboard data from: {url}", file=sys.stderr)
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        sys.exit(1)

    # Strategy 1: Find the JSON blob inside a script tag (common in Next.js)
    # The data is likely inside a structure like: [{"taskName":...}]
    # It might be escaped like \"taskName\" if inside a string.

    results = {}

    # We will try a regex that matches the pattern seen in curl output.
    # Pattern: \"taskName\":\"NAME\", ... \"avgResolutionRate\":RATE, ... \"successCount\":COUNT
    # flexible to handle both escaped \" and unescaped "

    # We use a pattern that finds the taskName and associated stats.
    # We assume they appear in the order: taskName -> ... -> avgResolutionRate
    # This might not be true if keys are unordered, but usually they are consistent in JSON serialization.

    # Regex explanation:
    # \\?\"taskName\\?\":\s*\\?\"([^\"]+)\\?\"   -> matches "taskName":"VALUE" (with optional backslashes)
    # .*?                                        -> match anything in between (lazy)
    # \\?\"avgResolutionRate\\?\":\s*([\d\.]+)   -> matches "avgResolutionRate":NUMBER
    # .*?                                        -> match anything
    # \\?\"successCount\\?\":\s*(\d+)            -> matches "successCount":NUMBER

    pattern = r'\\?"taskName\\?":\s*\\?"([^"\\]+)\\?",.*?\\?"avgResolutionRate\\?":\s*([\d\.]+),.*?\\?"successCount\\?":\s*(\d+)'

    matches = re.findall(pattern, html)

    if not matches:
        # Try finding the full JSON array first if the regex failed due to complexity
        # Look for a large array of objects with taskName
        print("Regex scan failed, trying to find JSON blob...", file=sys.stderr)
        match = re.search(r'(\[\{.*?"taskName".*?\}\])', html)
        if match:
            json_str = match.group(1)
            # Try to unescape if it looks escaped
            if '\\"' in json_str:
                json_str = json_str.replace('\\"', '"')

            try:
                data = json.loads(json_str)
                for task in data:
                    if isinstance(task, dict) and 'taskName' in task:
                         results[task['taskName']] = {
                            'avgResolutionRate': float(task.get('avgResolutionRate', 0)),
                            'successCount': int(task.get('successCount', 0)),
                            'nTrials': int(task.get('nTrials', 0))
                        }
            except:
                pass

    for task_name, rate, success_count in matches:
        results[task_name] = {
            'avgResolutionRate': float(rate),
            'successCount': int(success_count),
            'nTrials': 5 # Default
        }

    if not results:
        print(f"Could not extract data from {url}", file=sys.stderr)
        # Debug: print a snippet of HTML to stderr to see what's wrong
        # print(html[:2000], file=sys.stderr)
        sys.exit(1)

    return results

def fetch_registry_metadata():
    """
    Fetches the registry page and extracts task metadata (Category, Difficulty).
    Returns a dict: {taskName: {'category': str, 'difficulty': str}}
    """
    url = "https://www.tbench.ai/registry/terminal-bench/2.0"
    print(f"Fetching registry metadata from: {url}", file=sys.stderr)
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print(f"Error fetching registry: {e}", file=sys.stderr)
        sys.exit(1)

    metadata = {}

    # Split by the href attribute which seems unique per task block start
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

def main():
    parser = argparse.ArgumentParser(description="Compare TerminalBench 2.0 Leaderboard Models")
    parser.add_argument("url1", help="URL of the first model leaderboard page")
    parser.add_argument("url2", help="URL of the second model leaderboard page")
    parser.add_argument("--name1", help="Name of model 1 (optional)", default="Model 1")
    parser.add_argument("--name2", help="Name of model 2 (optional)", default="Model 2")

    args = parser.parse_args()

    data1 = fetch_leaderboard_data(args.url1)
    data2 = fetch_leaderboard_data(args.url2)
    metadata = fetch_registry_metadata()

    all_tasks = sorted(list(set(data1.keys()) | set(data2.keys())))

    print("| Task | Category | Difficulty | {} Success | {} Success | Difference |".format(args.name1, args.name2))
    print("|---|---|---|---|---|---|")

    for task in all_tasks:
        d1 = data1.get(task, {'avgResolutionRate': 0.0})
        d2 = data2.get(task, {'avgResolutionRate': 0.0})

        meta = metadata.get(task, {'category': 'Unknown', 'difficulty': 'Unknown'})

        rate1 = d1['avgResolutionRate'] * 100
        rate2 = d2['avgResolutionRate'] * 100
        diff = rate1 - rate2

        print(f"| {task} | {meta['category']} | {meta['difficulty']} | {rate1:.0f}% | {rate2:.0f}% | {diff:+.0f}% |")

if __name__ == "__main__":
    main()
