from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import dataclass
import time
from src.client import client
import uvicorn

# Define request model
@dataclass
class PromptRequest:
    prompt: str

app = FastAPI()

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
    return "Welcome to the TogetherAI LlamaIndex FastAPI App!"

@app.post("/api/schedule")
async def schedule_workflow(request: PromptRequest):
    try:
        workflow_id = f"{int(time.time() * 1000)}-LlmCompleteWorkflow"
        
        runId = await client.schedule_workflow(
            workflow_name="LlmCompleteWorkflow",
            workflow_id=workflow_id,
            input={"prompt": request.prompt}
        )
        
        result = await client.get_workflow_result(
            workflow_id=workflow_id,
            run_id=runId
        )
        
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def run_app():
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == '__main__':
    run_app()
