import os
import json
from google.oauth2 import service_account
from google.cloud import documentai_v1 as documentai

def google_client():
    credentials_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'service_account.json')
    if not os.path.exists(credentials_path):
        raise FileNotFoundError("Service account credentials file not found.")
    with open(credentials_path, 'r') as file:
        credentials_dict = json.load(file)
    if not credentials_dict:
        raise ValueError("Credentials are not properly configured in the service account file.")
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    client = documentai.DocumentProcessorServiceAsyncClient(credentials=credentials)
    if not client:
        raise Exception("Failed to initialize the Document AI client with the provided credentials.")
    return client