import asyncio
from src.client import client

async def main():
    await client.start_service({
        "workflows": [],
        "functions": []
    })

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()