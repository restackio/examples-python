import os
import asyncio
from functions import welcome, goodbye
from client import client

async def main():

    workflows_path = os.path.join(os.path.dirname(__file__), "workflows")

    client.start_service({
        "workflows_path": workflows_path,
        "functions": [welcome, goodbye]
    })

if __name__ == "__main__":
    asyncio.run(main())