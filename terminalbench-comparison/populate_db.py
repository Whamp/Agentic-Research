import sys
from tbench_lib import init_db, fetch_leaderboard_list, fetch_leaderboard_data, save_run_to_db

def main():
    print("Initializing Database...")
    init_db()

    print("Fetching Leaderboard List...")
    entries = fetch_leaderboard_list()
    print(f"Found {len(entries)} entries. Starting population...")

    success_count = 0
    fail_count = 0

    for i, entry in enumerate(entries):
        print(f"[{i+1}/{len(entries)}] Processing {entry['name']}...")
        url = entry['url']

        # Check if URL fetches correctly (handle potential 404s due to URL construction issues)
        data = fetch_leaderboard_data(url)
        if data:
            if save_run_to_db(url, data):
                print(f"  -> Saved successfully.")
                success_count += 1
            else:
                print(f"  -> DB Save failed.")
                fail_count += 1
        else:
            print(f"  -> Fetch failed (404 or parse error): {url}")
            # Try fallback URL construction (without @provider) if the first one failed?
            # Sometimes models don't use the @provider suffix in the URL if it's implicit or different.
            # But let's stick to the heuristic in tbench_lib first.
            fail_count += 1

    print("\n=== Population Complete ===")
    print(f"Successfully loaded: {success_count}")
    print(f"Failed: {fail_count}")

if __name__ == "__main__":
    main()
