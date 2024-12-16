from datetime import timedelta
from dataclasses import dataclass, field
from restack_ai.workflow import workflow, import_functions, log
with import_functions():
    from src.functions.function import welcome
    

@dataclass
class ChildInput:
    name: str = field(default="world")

@workflow.defn()
class ChildWorkflow:
    @workflow.run
    async def run(self, input: ChildInput):
        log.info("ChildWorkflow started")
        result = await workflow.step(welcome, input=input.name, start_to_close_timeout=timedelta(seconds=120))
        log.info("ChildWorkflow completed", result=result)
        return result


