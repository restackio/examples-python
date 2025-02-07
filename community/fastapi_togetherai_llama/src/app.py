import time
from dataclasses import dataclass

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.client import client


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
async def home() -> str:
    return "Welcome to the TogetherAI LlamaIndex FastAPI App!"


@app.post("/api/schedule")
async def schedule_workflow(request: PromptRequest) -> dict[str, str]:
    try:
        workflow_id = f"{int(time.time() * 1000)}-LlmCompleteWorkflow"

        run_id = await client.schedule_workflow(
            workflow_name="LlmCompleteWorkflow",
            workflow_id=workflow_id,
            input={"prompt": request.prompt},
        )

        result = await client.get_workflow_result(
            workflow_id=workflow_id,
            run_id=run_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    else:
        return {"result": result}

def run_app() -> None:
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True) # noqa: S104


if __name__ == "__main__":
    run_app()
