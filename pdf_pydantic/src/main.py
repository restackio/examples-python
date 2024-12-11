from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import time
from src.workflows.workflow import WorkflowInput
from src.client import client
import uvicorn
from src.services import run_services
import threading
from fastapi import FastAPI, File, UploadFile
import base64
import asyncio

app = FastAPI(
    title="PDF Pydantic FastAPI App",
    description="An API for scheduling and managing workflows.",
    version="1.0.0",
    docs_url="/docs",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return "Welcome to the PDF Pydantic FastAPI App!"

@app.post("/api/schedule")
async def schedule_workflow(files: list[UploadFile] = File(...)):
    try:
        async def process_file(file: UploadFile):
            file_content = await file.read()
            encoded_file = base64.b64encode(file_content).decode('utf-8')
            workflow_id = f"{int(time.time() * 1000)}-PdfWorkflow"
            
            runId = await client.schedule_workflow(
                workflow_name="PdfWorkflow",
                workflow_id=workflow_id,
                input=WorkflowInput(file_type=file.content_type, file_binary=encoded_file)
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

def start_services():
    run_services()

def run_main():
    # Start run_services in a separate thread
    service_thread = threading.Thread(target=start_services)
    service_thread.start()
    
    # Run the FastAPI application with hot reloading
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True, log_level="debug")

if __name__ == '__main__':
    run_main()