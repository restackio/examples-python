from datetime import timedelta

from pydantic import BaseModel, Field
from restack_ai.workflow import NonRetryableError, import_functions, log, workflow

with import_functions():
    from src.functions.llm import FunctionInputParams, llm
    from src.functions.weather import weather


class WorkflowInputParams(BaseModel):
    name: str = Field(default="John Doe")


@workflow.defn()
class MultistepWorkflow:
    @workflow.run
    async def run(self, workflow_input: WorkflowInputParams) -> dict:
        log.info("MultistepWorkflow started", workflow_input=workflow_input)
        user_content = f"Greet this person {workflow_input.name}"

        # Step 1 get weather data
        try:
            weather_data = await workflow.step(
                function=weather, start_to_close_timeout=timedelta(seconds=120)
            )
        except Exception as e:
            error_message = f"Error during weather: {e}"
            raise NonRetryableError(error_message) from e
        else:
            # Step 2 Generate greeting with LLM  based on name and weather data
            try:
                llm_message = await workflow.step(
                    function=llm,
                    function_input=FunctionInputParams(
                        system_content=f"You are a personal assitant and have access to weather data {weather_data}. Always greet person with relevant info from weather data",
                        user_content=user_content,
                        model="gpt-4o-mini",
                    ),
                    start_to_close_timeout=timedelta(seconds=120),
                )
            except Exception as e:
                error_message = f"Error during llm: {e}"
                raise NonRetryableError(error_message) from e
            else:
                log.info("MultistepWorkflow completed", llm_message=llm_message)
                return {"message": llm_message, "weather": weather_data}
