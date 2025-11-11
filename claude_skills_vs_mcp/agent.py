import subprocess
import time
import os
import signal

def run_command(command):
    print(f"Executing: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.stdout:
        print(f"Output:\n{result.stdout}")
    if result.stderr:
        print(f"Error:\n{result.stderr}")
    return result.stdout.strip()

def main():
    # Start the MCP server in the background
    server_process = subprocess.Popen(['python', 'claude_skills_vs_mcp/mcp_server.py'])
    print(f"MCP server started with PID: {server_process.pid}")
    time.sleep(1)  # Give the server a moment to start

    try:
        # Simulate the agent using the skill
        print("--- Agent is using the kv-store-skill ---")

        # Set a value
        run_command(['python', 'claude_skills_vs_mcp/kv-store-skill/scripts/set.py', 'hello', 'world'])

        # Get the value
        run_command(['python', 'claude_skills_vs_mcp/kv-store-skill/scripts/get.py', 'hello'])

        # Get a non-existent value
        run_command(['python', 'claude_skills_vs_mcp/kv-store-skill/scripts/get.py', 'foo'])

        # Delete the value
        run_command(['python', 'claude_skills_vs_mcp/kv-store-skill/scripts/delete.py', 'hello'])

        # Try to get the deleted value
        run_command(['python', 'claude_skills_vs_mcp/kv-store-skill/scripts/get.py', 'hello'])

    finally:
        # Stop the MCP server
        print(f"Stopping MCP server with PID: {server_process.pid}")
        os.kill(server_process.pid, signal.SIGTERM)
        server_process.wait()
        print("MCP server stopped.")

if __name__ == "__main__":
    main()
