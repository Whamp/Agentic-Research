import argparse
from tbench_lib import fetch_leaderboard_data, fetch_registry_metadata

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

    if not data1 or not data2:
        print("Failed to fetch one or more URLs.")
        return

    res1 = data1['results']
    res2 = data2['results']

    # Union of all tasks
    all_tasks = sorted(list(set(res1.keys()) | set(res2.keys())))

    print("| Task | Category | Difficulty | {} Success | {} Success | Difference |".format(args.name1, args.name2))
    print("|---|---|---|---|---|---|")

    for task in all_tasks:
        d1 = res1.get(task, {'avgResolutionRate': 0.0})
        d2 = res2.get(task, {'avgResolutionRate': 0.0})

        meta = metadata.get(task, {'category': 'Unknown', 'difficulty': 'Unknown'})

        rate1 = d1['avgResolutionRate'] * 100
        rate2 = d2['avgResolutionRate'] * 100
        diff = rate1 - rate2

        print(f"| {task} | {meta['category']} | {meta['difficulty']} | {rate1:.0f}% | {rate2:.0f}% | {diff:+.0f}% |")

if __name__ == "__main__":
    main()
