import requests
from restack_ai.function import function, log
from src.functions.hn.schema import HnSearchInput

@function.defn()
async def hn_search(input: HnSearchInput):
    try:
        # Fetch the latest stories IDs
        response = requests.get(
            f"https://hn.algolia.com/api/v1/search_by_date?tags=show_hn&query={input.query}&hitsPerPage={input.count}&numericFilters=points>2"
        )
        data = response.json()

        log.info("hnSearch", extra={"data": data})
        return data
    except Exception as error:
        log.error("hn_search function failed", error=error)
        raise error