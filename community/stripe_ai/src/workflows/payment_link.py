from restack_ai.workflow import workflow, import_functions, log, RetryPolicy
from datetime import timedelta

with import_functions():
    from src.functions.create_payment_link import create_payment_link

@workflow.defn()
class CreatePaymentLinkWorkflow:
    @workflow.run
    async def run(self):
        log.info("CreatePaymentLinkWorkflow started", input=input)

        result = await workflow.step(
            create_payment_link,
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=10),
                backoff_coefficient=1,
            ),
        )

        return result
