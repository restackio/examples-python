import os
from restack_sdk_cloud import RestackCloud

async def main():
    # Initialize the RestackCloud client with the SDK token from environment variables
    restack_cloud_client = RestackCloud(os.getenv('RESTACK_SDK_TOKEN'))

    # Define the backend application configuration
    backend_app = {
        'name': 'backend-fastapi-togetherai-llama',
        'dockerFilePath': 'examples/fastapi_togetherai_llama/Dockerfile',
        'dockerBuildContext': 'examples/fastapi_togetherai_llama',
        'gitBranch': '51-dockerfiles-and-restack_uppy',

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