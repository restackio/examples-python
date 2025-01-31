from datetime import timedelta
from pydantic import BaseModel
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.lookup_sales import lookupSales, LookupSalesInput, LookupSalesOutput

class SalesWorkflowInput(BaseModel):
    category: str

@workflow.defn()
class SalesWorkflow:
    @workflow.run
    async def run(self, input: SalesWorkflowInput) -> LookupSalesOutput:
        log.info("SalesWorkflow started")
        result = await workflow.step(lookupSales, input=LookupSalesInput(category=input.category), start_to_close_timeout=timedelta(seconds=120))
        log.info("SalesWorkflow completed", result=result)
        return result


