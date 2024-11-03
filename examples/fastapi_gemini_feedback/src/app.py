from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from restack_ai import Restack
import time

import uvicorn

app = FastAPI()



@app.get("/")
async def home():
    return {"message": "Welcome to the FastAPI App!"}

@app.get("/test")
async def test_route():
    return {"message": "This is a test route"}

class InputParams(BaseModel):
    user_content: str

@app.post("/api/schedule")
async def schedule_workflow(data: InputParams):
    
    print(data)

    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-GeminiGenerateWorkflow"
    run_id = await client.schedule_workflow(
        workflow_name="GeminiGenerateWorkflow",
        workflow_id=workflow_id,
        input=data
    )

    print(f"Scheduled workflow with run_id: {run_id}")

    return {
        "workflow_id": workflow_id,
        "run_id": run_id
    }

class FeedbackParams(BaseModel):
    workflow_id: str
    run_id: str
    feedback: str

@app.post("/api/event/feedback")
async def send_event_feedback(data: FeedbackParams):
    client = Restack()

    print(f"event feedback: {data}")

    await client.send_workflow_event(
        workflow_id=data.workflow_id,
        run_id=data.run_id,
        event_name="event_feedback",
        event_input={"feedback": data.feedback}
    )
    return

class EndParams(BaseModel):
    workflow_id: str
    run_id: str

@app.post("/api/event/end")
async def send_event_end(data: EndParams):
    client = Restack()

    await client.send_workflow_event(
        workflow_id=data.workflow_id,
        run_id=data.run_id,
        event_name="event_end"
    )
    return

def run_app():
    uvicorn.run("src.app:app", host="0.0.0.0", port=5001, reload=True)

if __name__ == '__main__':
    run_app()