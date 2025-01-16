from pydantic import BaseModel, Field

class HnSearchInput(BaseModel):
    query: str = Field(default=None, description="The query for search")
    count: int = Field(default=5, description="The number of results to return")