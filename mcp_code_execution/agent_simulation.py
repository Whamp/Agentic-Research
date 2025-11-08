# mcp_code_execution/agent_simulation.py
import os
import importlib
import json

def discover_tools(base_path='mcp_code_execution/servers'):
    """Discovers available MCP servers and their tools."""
    servers = {}
    for server_name in os.listdir(base_path):
        server_path = os.path.join(base_path, server_name)
        if os.path.isdir(server_path) and not server_name.startswith('__'):
            tools = []
            for tool_file in os.listdir(server_path):
                if tool_file.endswith('.py') and not tool_file.startswith('__'):
                    tools.append(tool_file[:-3])
            servers[server_name] = tools
    return servers

def read_tool_definition(server_name, tool_name):
    """Reads the source code of a tool to understand its interface."""
    file_path = f"mcp_code_execution/servers/{server_name}/{tool_name}.py"
    with open(file_path, 'r') as f:
        return f.read()

def simulate_agent_workflow():
    """Simulates the agent's workflow of discovering and using tools."""
    # Ensure workspace and skills directories exist
    os.makedirs("mcp_code_execution/workspace", exist_ok=True)
    os.makedirs("mcp_code_execution/skills", exist_ok=True)

    print("Agent: Starting workflow...")

    # 1. Discover available tools
    available_tools = discover_tools()
    print(f"Agent: Discovered tools: {available_tools}")

    # 2. Agent decides to use gdrive to get a document and then update salesforce
    print("Agent: I need to get a document from Google Drive and update a Salesforce record.")

    # 3. Read tool definitions to understand how to use them
    gdrive_tool_def = read_tool_definition('google_drive', 'get_document')
    salesforce_tool_def = read_tool_definition('salesforce', 'update_record')

    print("\nAgent: Reading Google Drive tool definition...")
    print(gdrive_tool_def)

    print("\nAgent: Reading Salesforce tool definition...")
    print(salesforce_tool_def)

    # 4. Generate code to perform the task
    print("\nAgent: Generating code to perform the task...")
    generated_code = """
import mcp_code_execution.servers.google_drive as google_drive
import mcp_code_execution.servers.salesforce as salesforce
import json

# Get the document from Google Drive
document = google_drive.get_document(document_id='doc123')
print(f"Agent: Got document content: {document['content']}")

# Simulate processing the document to extract relevant info
processed_data = {"notes": f"Summary: {document['content'][:10]}..."}
print(f"Agent: Processed data for Salesforce: {processed_data}")

# Save intermediate result to a file (State Persistence)
with open('mcp_code_execution/workspace/processed_data.json', 'w') as f:
    json.dump(processed_data, f)
print("Agent: Saved intermediate result to workspace/processed_data.json")

# Update the Salesforce record
update_status = salesforce.update_record(record_id='rec456', data=processed_data)
print(f"Agent: Salesforce update status: {update_status}")
"""

    print("\n--- Generated Code ---")
    print(generated_code)
    print("----------------------")

    # 5. Execute the generated code
    print("\nAgent: Executing generated code...")
    exec(generated_code)

    # 6. Later, another task needs the processed data
    print("\nAgent: A new task needs the processed data from the previous step.")

    # 7. Generate code to save a reusable skill
    print("\nAgent: Generating code to create a reusable skill...")
    skill_code = """
import mcp_code_execution.servers.google_drive as google_drive
import mcp_code_execution.servers.salesforce as salesforce
import json

def process_document_and_update_salesforce(doc_id, record_id):
    '''Gets a doc, processes it, and updates salesforce.'''
    document = google_drive.get_document(document_id=doc_id)
    processed_data = {"notes": f"Summary: {document['content'][:10]}..."}
    update_status = salesforce.update_record(record_id=record_id, data=processed_data)
    return update_status
"""
    with open("mcp_code_execution/skills/process_and_update.py", "w") as f:
        f.write(skill_code)
    print("Agent: Saved the new skill to skills/process_and_update.py")

    # 8. Use the newly created skill
    print("\nAgent: Now, let's use the new skill for another task.")

    # Dynamically import and use the skill
    spec = importlib.util.spec_from_file_location("process_and_update", "mcp_code_execution/skills/process_and_update.py")
    skill_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(skill_module)

    print("Agent: Calling the skill...")
    result = skill_module.process_document_and_update_salesforce('doc456', 'rec789')
    print(f"Agent: Skill execution result: {result}")


if __name__ == "__main__":
    simulate_agent_workflow()
