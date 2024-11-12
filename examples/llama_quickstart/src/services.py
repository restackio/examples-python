import asyncio
from src.client import client
from src.functions.llm.chat import llm_chat
from src.functions.hn.search import hn_search
from src.workflows.workflow import HnWorkflow
from src.functions.crawl.website import crawl_website
from restack_ai.restack import ServiceOptions

async def main():
    await asyncio.gather(
        client.start_service(
            workflows=[HnWorkflow],
            functions=[hn_search, crawl_website]
        ),
        client.start_service(
            functions=[llm_chat],
            task_queue="llm_chat",
            options=ServiceOptions(
                rate_limit=1,
                max_concurrent_function_runs=1
            )
        )
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()
