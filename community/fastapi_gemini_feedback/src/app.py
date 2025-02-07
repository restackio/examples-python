import logging
import time

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from restack_ai import Restack

app = FastAPI()


@app.get("/")
async def home() -> dict[str, str]:
    return {"message": "Welcome to the FastAPI App!"}


@app.get("/test")
async def test_route() -> dict[str, str]:
    return {"message": "This is a test route"}


class InputParams(BaseModel):
    user_content: str


@app.post("/api/schedule")
async def schedule_workflow(data: InputParams) -> dict[str, str]:
    logging.info("schedule_workflow: %s", data)

    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-GeminiGenerateWorkflow"
    run_id = await client.schedule_workflow(
        workflow_name="GeminiGenerateWorkflow",
        workflow_id=workflow_id,
        input=data,
    )

    logging.info("Scheduled workflow with run_id: %s", run_id)

    return {
        "workflow_id": workflow_id,
        "run_id": run_id,
    }


class FeedbackParams(BaseModel):
    workflow_id: str
    run_id: str
    feedback: str


@app.post("/api/event/feedback")
async def send_event_feedback(data: FeedbackParams) -> None:
    client = Restack()

    logging.info("event feedback: %s", data)

    await client.send_workflow_event(
        workflow_id=data.workflow_id,
        run_id=data.run_id,
        event_name="event_feedback",
        event_input={"feedback": data.feedback},
    )


class EndParams(BaseModel):
    workflow_id: str
    run_id: str


@app.post("/api/event/end")
async def send_event_end(data: EndParams) -> None:
    client = Restack()

    await client.send_workflow_event(
        workflow_id=data.workflow_id,
        run_id=data.run_id,
        event_name="event_end",
    )


def run_app() -> None:
    uvicorn.run("src.app:app", host="0.0.0.0", port=5001, reload=True) # noqa: S104


if __name__ == "__main__":
    run_app()
