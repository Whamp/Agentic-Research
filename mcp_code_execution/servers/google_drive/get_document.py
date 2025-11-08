# mcp_code_execution/servers/google_drive/get_document.py
from ...client import call_mcp_tool

def get_document(document_id: str) -> dict:
    """
    Retrieves a document from Google Drive.
    """
    return call_mcp_tool('google_drive__get_document', document_id=document_id)
