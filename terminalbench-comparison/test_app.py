import sys
import pandas as pd
from tbench_lib import fetch_leaderboard_data, fetch_registry_metadata

def main():
    print("Testing TerminalBench 2.0 Dashboard Logic...")

    urls = {
        "Droid GPT 5.2": "https://www.tbench.ai/leaderboard/terminal-bench/2.0/Factory%20Droid/unknown/gpt-5.2%40openai",
        "Droid Opus 4.5": "https://www.tbench.ai/leaderboard/terminal-bench/2.0/Factory%20Droid/unknown/claude-opus-4-5-20251101%40anthropic",
        "Terminus Opus 4.5": "https://www.tbench.ai/leaderboard/terminal-bench/2.0/terminus-2/2.0.0/claude-opus-4-5-20251101%40anthropic"
    }

    runs = {}

    # 1. Fetch Data
    for name, url in urls.items():
        print(f"Fetching {name}...")
        data = fetch_leaderboard_data(url)
        if data:
            runs[name] = data
            print(f"  Success: {len(data['results'])} tasks found. Metadata: {data['metadata']}")
        else:
            print(f"  Failed to fetch {name}")
            sys.exit(1)

    # 2. Fetch Registry
    print("Fetching Registry...")
    reg_meta = fetch_registry_metadata()
    print(f"  Registry loaded: {len(reg_meta)} tasks.")

    # 3. Construct DataFrame
    all_tasks = set()
    for run_data in runs.values():
        all_tasks.update(run_data['results'].keys())

    data_rows = []
    run_cols = list(runs.keys())

    for task in all_tasks:
        row = {'Task': task}
        meta = reg_meta.get(task, {'category': 'Unknown', 'difficulty': 'Unknown'})
        row['Category'] = meta['category']
        row['Difficulty'] = meta['difficulty']

        for run_name, run_data in runs.items():
            res = run_data['results'].get(task)
            if res:
                row[run_name] = res['avgResolutionRate'] * 100
            else:
                row[run_name] = 0.0
        data_rows.append(row)

    df = pd.DataFrame(data_rows)
    print(f"DataFrame constructed: {df.shape[0]} rows, {df.shape[1]} cols.")

    # --- Feature Verify: Impossible Task Filtering ---

    # Count impossible tasks (0% everywhere)
    df['MaxScore'] = df[run_cols].max(axis=1)
    impossible_tasks = df[df['MaxScore'] == 0]
    print(f"\nImpossible Tasks (0% across all 3 models): {len(impossible_tasks)}")

    if len(impossible_tasks) > 0:
        print("Sample impossible tasks:", impossible_tasks['Task'].head(3).tolist())

    # Filter
    df_filtered = df[df['MaxScore'] > 0].copy()
    print(f"Filtered DataFrame size: {len(df_filtered)}")

    if len(df_filtered) != len(df) - len(impossible_tasks):
        print("ERROR: Filtering math mismatch!")
        sys.exit(1)
    else:
        print("Filtering logic verified.")

    # --- Feature Verify: Recommendations ---

    print("\n=== Recommendation Logic Test (Category: scientific-computing) ===")
    category = "scientific-computing"

    df_cat = df_filtered[df_filtered['Category'] == category]
    if not df_cat.empty:
        scores = df_cat[run_cols].mean().sort_values(ascending=False)
        print("Ranking:")
        print(scores)

        best = scores.index[0]
        print(f"Best model for {category}: {best} ({scores.iloc[0]:.2f}%)")
    else:
        print(f"No tasks found for {category}")

if __name__ == "__main__":
    main()
