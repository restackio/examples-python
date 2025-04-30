import os
import requests
from restack_ai.function import function, FunctionFailure
from pydantic import BaseModel, Field
from google.cloud import documentai_v1 as documentai

from .google_client import google_client

class OcrInput(BaseModel):
    file_type: str = Field(default='application/pdf')
    file_name: str

@function.defn()
async def google_doc_ai_pdf(input: OcrInput):
    try:
        response = requests.get(f"{os.getenv('RESTACK_API_ADDRESS', 'http://localhost:6233')}/api/download/{input.file_name}")
        response.raise_for_status()
        content = response.content

        if input.file_type != "application/pdf":
            raise FunctionFailure("Unsupported file type", non_retryable=True)

        from doctr.io import DocumentFile
        doc = DocumentFile.from_pdf(content)
    except Exception as e:
        raise FunctionFailure("Error downloading file", non_retryable=True)
    
    client = google_client()
    name = f"projects/{os.getenv('GOOGLE_PROJECT_ID')}/locations/{os.getenv('GOOGLE_LOCATION')}/processors/{os.getenv('GOOGLE_PROCESSOR_ID')}"

    inline_document = documentai.Document(content=content, mime_type=input.file_type)
    request = documentai.ProcessRequest(inline_document=inline_document, name=name)
    response = await client.process_document(request=request)

    return response.document.text
