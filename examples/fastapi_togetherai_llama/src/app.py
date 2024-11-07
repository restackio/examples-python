from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
from restack_ai import Restack

# Define request model
class PromptRequest(BaseModel):
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
        client = Restack()
        workflow_id = f"{int(time.time() * 1000)}-llm_complete_workflow"
        
        runId = await client.schedule_workflow(
            workflow_name="llm_complete_workflow",
            workflow_id=workflow_id,
            input={"prompt": request.prompt}
        )
        print("Scheduled workflow", runId)
        
        result = await client.get_workflow_result(
            workflow_id=workflow_id,
            run_id=runId
        )
        
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Remove Flask-specific run code since FastAPI uses uvicorn
