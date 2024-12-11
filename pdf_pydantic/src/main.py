from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import time
from src.workflows.pdf import PdfWorkflowInput
from src.workflows.files import FilesWorkflowInput
from src.client import client
import uvicorn
from src.services import run_services
import threading
from fastapi import FastAPI, File, UploadFile
import base64
import asyncio
import signal

app = FastAPI(
    title="PDF Pydantic Example",
    description="An API for scheduling and managing workflows to OCR PDFs and get a summary with OpenaI.",
    version="1.0.0",
    docs_url="/",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/pdfs")
async def schedule_workflow(files: list[UploadFile] = File(...)):
    try:
        async def process_file(file: UploadFile):
            file_content = await file.read()
            encoded_file = base64.b64encode(file_content).decode('utf-8')
            workflow_id = f"{int(time.time() * 1000)}-PdfWorkflow"
            
            runId = await client.schedule_workflow(
                workflow_name="PdfWorkflow",
                workflow_id=workflow_id,
                input=PdfWorkflowInput(file_type=file.content_type, file_binary=encoded_file)
            )
            
            result = await client.get_workflow_result(
                workflow_id=workflow_id,
                run_id=runId
            )
            return {"file_name": file.filename, "result": result}

        results = await asyncio.gather(*(process_file(file) for file in files))
        
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/pdfs-parent")
async def execute_files_workflow(files: list[UploadFile] = File(...)):
    try:
        # Read and encode all files
        encoded_files = []
        for file in files:
            file_content = await file.read()
            encoded_file = base64.b64encode(file_content).decode('utf-8')
            encoded_files.append({"file_type": file.content_type, "file_binary": encoded_file})

        # Create a unique workflow ID
        workflow_id = f"{int(time.time() * 1000)}-FilesWorkflow"

        # Schedule the FilesWorkflow with all encoded files
        runId = await client.schedule_workflow(
            workflow_name="FilesWorkflow",
            workflow_id=workflow_id,
            input=FilesWorkflowInput(files=encoded_files)
        )

        # Get the result of the workflow
        result = await client.get_workflow_result(
            workflow_id=workflow_id,
            run_id=runId
        )

        return {"workflow_id": workflow_id, "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
stop_event = threading.Event()

def start_services():
    run_services()

def run_main():
    # Start run_services in a separate thread
    service_thread = threading.Thread(target=start_services)
    service_thread.start()
    
    # Define a signal handler to stop the application
    def signal_handler(sig, frame):
        print("Signal received, stopping services...")
        stop_event.set()
        service_thread.join()  # Wait for the service thread to finish
        print("Services stopped. Exiting application.")
        exit(0)

    # Register the signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Run the FastAPI application with hot reloading
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == '__main__':
    run_main()