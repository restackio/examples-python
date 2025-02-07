import aiohttp
from restack_ai.function import FunctionFailure, function, log

from src.functions.hn.schema import HnSearchInput


@function.defn()
async def hn_search(hn_search_input: HnSearchInput) -> dict:
    try:
        async with aiohttp.ClientSession() as session, session.get(
            f"https://hn.algolia.com/api/v1/search_by_date?tags=show_hn&query={hn_search_input.query}&hitsPerPage={hn_search_input.count}&numericFilters=points>2",
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response:
            response.raise_for_status()
            data = await response.json()

        log.info("hnSearch", extra={"data": data})
    except Exception as error:
        error_message = "hn_search function failed"
        log.error(error_message, error=error)
        raise FunctionFailure(error_message, non_retryable=True) from error
    else:
        return data
