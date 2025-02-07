from datetime import timedelta

from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.crawl.website import crawl_website
    from src.functions.hn.schema import HnSearchInput
    from src.functions.hn.search import hn_search
    from src.functions.llm.chat import FunctionInputParams, llm_chat


@workflow.defn()
class HnWorkflow:
    @workflow.run
    async def run(self, hn_workflow_input: dict) -> str:
        query = hn_workflow_input["query"]
        count = hn_workflow_input["count"]
        hn_results = await workflow.step(
            hn_search,
            HnSearchInput(query=query, count=count),
            start_to_close_timeout=timedelta(seconds=10),
        )
        urls = [hit["url"] for hit in hn_results["hits"] if "url" in hit]

        crawled_contents = []
        for url in urls:  # Use the extracted URLs
            log.info("hn_result", extra={"url": url})
            if url:
                content = await workflow.step(
                    crawl_website,
                    url,
                    start_to_close_timeout=timedelta(seconds=30),
                )
                crawled_contents.append(content)

        summaries = []
        for content in crawled_contents:
            system_prompt = (
                "Provide a summary of the website for project found on Hacker news"
            )
            user_prompt = f"Summarize the following content: {content}"
            summary = await workflow.step(
                llm_chat,
                FunctionInputParams(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                ),
                task_queue="llm_chat",
                start_to_close_timeout=timedelta(seconds=120),
            )
            summaries.append(summary)

        system_prompt = """
        You are a personal assistant.
        Provide a summary of the latest hacker news and the summaries of the websites.
        Structure your response with the title of the project,
        then a short description and a list of actionable bullet points.
        """
        user_prompt = f"""
        Here is the latest hacker news data: {hn_results!s}
        and summaries of the websites: {summaries!s}
        """

        return await workflow.step(
            llm_chat,
            FunctionInputParams(system_prompt=system_prompt, user_prompt=user_prompt),
            task_queue="llm_chat",
            start_to_close_timeout=timedelta(seconds=120),
        )
