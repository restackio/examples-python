import asyncio
from watchfiles import run_process
import webbrowser
import os

from src.client import client
from src.functions.generate_content import gemini_generate_content
from src.workflows.generate_content import GeminiGenerateContentWorkflow

from src.workflows.function_call import GeminiFunctionCallWorkflow
from src.functions.function_call import gemini_function_call

from src.workflows.multi_function_call import GeminiMultiFunctionCallWorkflow
from src.functions.multi_function_call import gemini_multi_function_call

from src.workflows.multi_function_call_advanced import GeminiMultiFunctionCallAdvancedWorkflow
from src.functions.multi_function_call_advanced import gemini_multi_function_call_advanced
from src.functions.multi_function_call_advanced import get_current_weather, get_humidity, get_air_quality

async def main():
    await client.start_service(
        workflows= [GeminiGenerateContentWorkflow, GeminiFunctionCallWorkflow, GeminiMultiFunctionCallWorkflow, GeminiMultiFunctionCallAdvancedWorkflow],
        functions= [gemini_generate_content, gemini_function_call, gemini_multi_function_call, gemini_multi_function_call_advanced, get_current_weather, get_humidity, get_air_quality]
    )

def run_services():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Service interrupted by user. Exiting gracefully.")

def watch_services():
    watch_path = os.getcwd()
    print(f"Watching {watch_path} and its subdirectories for changes...")
    webbrowser.open("http://localhost:5233")
    run_process(watch_path, recursive=True, target=run_services)

if __name__ == "__main__":
       run_services()