import requests
import sys

def set_value(key, value):
    url = "http://127.0.0.1:5001/mcp"
    payload = {
        "tool_name": "set",
        "params": {
            "key": key,
            "value": value
        }
    }
    response = requests.post(url, json=payload)
    result = response.json()
    if result.get('success'):
        print(result.get('message'))
    else:
        print(f"Error: {result.get('error')}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python set.py <key> <value>")
        sys.exit(1)

    key = sys.argv[1]
    value = sys.argv[2]
    set_value(key, value)
