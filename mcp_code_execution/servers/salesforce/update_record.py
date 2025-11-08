# mcp_code_execution/servers/salesforce/update_record.py
from ...client import call_mcp_tool

def update_record(record_id: str, data: dict) -> dict:
    """
    Updates a record in Salesforce.
    """
    return call_mcp_tool('salesforce__update_record', record_id=record_id, data=data)
