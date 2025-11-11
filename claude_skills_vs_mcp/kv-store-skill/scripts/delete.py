import requests
import sys

def delete_value(key):
    url = "http://127.0.0.1:5001/mcp"
    payload = {
        "tool_name": "delete",
        "params": {
            "key": key
        }
    }
    response = requests.post(url, json=payload)
    result = response.json()
    if result.get('success'):
        print(result.get('message'))
    else:
        print(f"Error: {result.get('error')}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python delete.py <key>")
        sys.exit(1)

    key = sys.argv[1]
    delete_value(key)
