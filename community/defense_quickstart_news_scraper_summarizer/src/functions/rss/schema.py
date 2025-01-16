from pydantic import BaseModel, Field

class RssInput(BaseModel):
    url: str = Field(default=None, description="The url to get rss from")
    count: int | None = Field(default=None, description="The number of results to return")