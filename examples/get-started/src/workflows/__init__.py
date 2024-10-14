from restack_ai import workflow

@workflow.step
async def welcome(name: str) -> str:
    return f"Hello, {name}!"

@workflow.step
async def goodbye(name: str) -> str:
    return f"Goodbye, {name}!"

@workflow.workflow
async def greeting_workflow(name: str) -> dict:
    welcome_message = await welcome(name)
    goodbye_message = await goodbye(name)
    return {
        "welcome": welcome_message,
        "goodbye": goodbye_message
    }