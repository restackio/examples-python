from restack_ai.workflow import workflow, import_functions, log, RetryPolicy, workflow_info
from pydantic import BaseModel
from datetime import timedelta
import asyncio
from src.functions.tools import USTopCities
from src.workflows.multi_function_call_advanced import GeminiMultiFunctionCallAdvancedWorkflow, MultiFunctionCallAdvancedInputParams        

class WorkflowInputParams(BaseModel):
    num_cities: int = 50

@workflow.defn()
class GeminiSwarmWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        parent_workflow_id = workflow_info().workflow_id
        
        # Get all available cities from USTopCities enum
        all_cities = [city.value for city in USTopCities]
        
        # Take the first n cities based on input
        selected_cities = all_cities[:input.num_cities]

        results_tasks = await asyncio.gather(*[
            workflow.child_execute(
                GeminiMultiFunctionCallAdvancedWorkflow,
                input=MultiFunctionCallAdvancedInputParams(user_content=f"What's the weather in {city}?"),
                workflow_id=f"{parent_workflow_id}-child-{city.replace(', ', '-')}"
            ) for city in selected_cities
        ])

        results = [{"city": city, "result": result} for city, result in zip(selected_cities, results_tasks)]
        
        log.info("GeminiSwarmWorkflow completed", results=results)
        return results
