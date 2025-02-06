from pydantic import BaseModel, Field
from restack_ai.workflow import workflow, import_functions, log
from datetime import timedelta

with import_functions():
    from src.functions.llm import llm, FunctionInputParams
    from src.functions.weather import weather

class WorkflowInputParams ( BaseModel):
    name: str = Field(default="John Doe")

@workflow.defn()
class MultistepWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        log.info("MultistepWorkflow started", input=input)
        user_content = f"Greet this person {input.name}"

        # Step 1 get weather data
        weather_data = await workflow.step(
            weather,
            start_to_close_timeout=timedelta(seconds=120)
        )

        # Step 2 Generate greeting with LLM  based on name and weather data

        llm_message = await workflow.step(
            llm,
            FunctionInputParams(
                system_content=f"You are a personal assitant and have access to weather data {weather_data}. Always greet person with relevant info from weather data",
                user_content=user_content,
                model="gpt-4o-mini"
            ),
            start_to_close_timeout=timedelta(seconds=120)
        )
        log.info("MultistepWorkflow completed", llm_message=llm_message)
        return {
            "message": llm_message,
            "weather": weather_data
        }
