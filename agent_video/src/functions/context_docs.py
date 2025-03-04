import aiohttp
from restack_ai.function import function, log


async def fetch_content_from_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            log.error("Failed to fetch content", status=response.status)
            raise Exception(f"Failed to fetch content: {response.status}")


@function.defn()
async def context_docs() -> str:
    try:
        docs_content = await fetch_content_from_url("https://docs.restack.io/llms-full.txt")
        log.info("Fetched content from URL", content=len(docs_content))

        return docs_content

    except Exception as e:
        log.error("llm_chat function failed", error=str(e))
        raise
