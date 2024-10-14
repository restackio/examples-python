async def goodbye(name: str) -> dict:
    return {"message": f"Goodbye, {name}!"}

async def welcome(name: str) -> dict:
    return {"message": f"Hello, {name}!"}