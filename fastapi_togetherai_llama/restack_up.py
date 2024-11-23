import os
from restack_sdk_cloud import RestackCloud
from dotenv import load_dotenv  
load_dotenv()

async def main():
    # Initialize the RestackCloud client with the CLOUD token from environment variables
    restack_cloud_client = RestackCloud(os.getenv('RESTACK_CLOUD_TOKEN'))

    # Define the backend application configuration
    backend_app = {
        'name': 'backend-fastapi-togetherai-llama',
        'dockerFilePath': 'examples/fastapi_togetherai_llama/Dockerfile',
        'dockerBuildContext': 'examples/fastapi_togetherai_llama',
        'environmentVariables': [
            {
                'name': 'RESTACK_ENGINE_ID',
                'value': os.getenv('RESTACK_ENGINE_ID'),
            },
            {
                'name': 'RESTACK_ENGINE_ADDRESS',
                'value': os.getenv('RESTACK_ENGINE_ADDRESS'),
            },
            {
                'name': 'RESTACK_ENGINE_API_KEY',
                'value': os.getenv('RESTACK_ENGINE_API_KEY'),
            },
            {
                'name': 'TOGETHER_API_KEY',
                'value': os.getenv('TOGETHER_API_KEY'),
            },
        ],
    }

    # Configure the stack with the applications
    await restack_cloud_client.stack({
        'name': 'fastapi-togetherai-llama',
        'applications': [backend_app],
        'previewEnabled': False,
    })

    # Deploy the stack
    await restack_cloud_client.up()

# Run the main function
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())