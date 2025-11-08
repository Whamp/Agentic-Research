
import mcp_code_execution.servers.google_drive as google_drive
import mcp_code_execution.servers.salesforce as salesforce
import json

def process_document_and_update_salesforce(doc_id, record_id):
    '''Gets a doc, processes it, and updates salesforce.'''
    document = google_drive.get_document(document_id=doc_id)
    processed_data = {"notes": f"Summary: {document['content'][:10]}..."}
    update_status = salesforce.update_record(record_id=record_id, data=processed_data)
    return update_status
