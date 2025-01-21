from pydantic import BaseModel, Field
from restack_ai.workflow import workflow
from typing import List, Dict
from src.workflows.code_execution import CodeExecutionWorkflow, CodeExecutionWorkflowInput
import asyncio


class ManyCodeExecutionWorkflowInput(BaseModel):
    tasks: List[str] = Field(default=[
        'Calculate how many r\'s are in the word \'strawberry\'',
        'Find the sum of numbers from 1 to 100',
        'Calculate the factorial of 5',
        'Count the vowels in the word \'elephant\'',
        'Generate a list of first 10 Fibonacci numbers',
        'Check if 17 is a prime number',
        'Convert 25 Celsius to Fahrenheit',
        'Calculate the area of a circle with radius 5',
        'Find all even numbers between 1 and 20',
        'Calculate the length of the hypotenuse for a right triangle with sides 3 and 4'
    ])

class ManyCodeExecutionWorkflowOutput(BaseModel):
    results: List[str] = Field(default=[])
    
    
@workflow.defn()
class ManyCodeExecutionWorkflow:
    @workflow.run
    async def run(self, input: ManyCodeExecutionWorkflowInput) -> ManyCodeExecutionWorkflowOutput:
        tasks = [
            workflow.child_execute(
                CodeExecutionWorkflow,
                workflow_id=f"code_execution_{i}",
                input=CodeExecutionWorkflowInput(user_content=task)
            )
            for i, task in enumerate(input.tasks)
        ]
        results = await asyncio.gather(*tasks)
        return ManyCodeExecutionWorkflowOutput(results=[r.content for r in results])