# mcp_code_execution/client.py

import json

def call_mcp_tool(tool_name, **kwargs):
    """
    Simulates a call to an MCP server.
    In a real implementation, this would handle the network request to the MCP server.
    For this simulation, it prints the tool call and returns a mock response.
    """
    print(f"Calling MCP tool '{tool_name}' with arguments: {kwargs}")

    # Mock responses based on the tool name
    if tool_name == "google_drive__get_document":
        return {"content": "This is a mock document from Google Drive."}
    elif tool_name == "salesforce__update_record":
        return {"status": "success", "record_id": kwargs.get("record_id")}
    else:
        return {"error": "Unknown tool"}
