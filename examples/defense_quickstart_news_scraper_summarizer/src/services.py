import asyncio
from src.client import client
from src.functions.llm.chat import llm_chat
from src.functions.rss.pull import rss_pull
from src.workflows.workflow import RssWorkflow
from src.functions.crawl.website import crawl_website
from src.functions.helper.split_text import split_text
from restack_ai.restack import ServiceOptions

async def main():
    await asyncio.gather(
        client.start_service(
            workflows=[RssWorkflow],
            functions=[rss_pull, crawl_website, split_text]
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
