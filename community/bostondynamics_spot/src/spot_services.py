import asyncio
from src.client import client
from src.functions.bostondynamics.commands import spot_commands
async def main():

    await client.start_service(
        functions= [spot_commands]
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()