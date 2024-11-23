import os
from restack_sdk_cloud import RestackCloud
from dotenv import load_dotenv  
load_dotenv()

async def main():
    # Initialize the RestackCloud client with the CLOUD token from environment variables
    restack_cloud_client = RestackCloud(os.getenv('RESTACK_CLOUD_TOKEN'))

    engine = {
        'name': 'restack_engine',
        'image': 'restack/restack:main',
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
        ],
    }

    # Define the application configuration
    app = {
        'name': 'llama_quickstart',
        'dockerFilePath': '/llama_quickstart/Dockerfile',
        'dockerBuildContext': './llama_quickstart/',
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
        'name': 'development environment python',
        'previewEnabled': False,
        'applications': [engine,app],
    })

    # Deploy the stack
    await restack_cloud_client.up()

# Run the main function
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())