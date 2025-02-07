import asyncio
import logging
import webbrowser
from pathlib import Path

from restack_ai.restack import ServiceOptions
from watchfiles import run_process

from src.client import client
from src.functions.function_call import gemini_function_call
from src.functions.generate_content import gemini_generate_content
from src.functions.multi_function_call import gemini_multi_function_call
from src.functions.multi_function_call_advanced import (
    gemini_multi_function_call_advanced,
)
from src.functions.tools import get_air_quality, get_current_temperature, get_humidity
from src.workflows.function_call import GeminiFunctionCallWorkflow
from src.workflows.generate_content import GeminiGenerateContentWorkflow
from src.workflows.multi_function_call import GeminiMultiFunctionCallWorkflow
from src.workflows.multi_function_call_advanced import (
    GeminiMultiFunctionCallAdvancedWorkflow,
)
from src.workflows.swarm import GeminiSwarmWorkflow


async def main() -> None:
    await asyncio.gather(
        client.start_service(
            workflows=[
                GeminiGenerateContentWorkflow,
                GeminiFunctionCallWorkflow,
                GeminiMultiFunctionCallWorkflow,
                GeminiMultiFunctionCallAdvancedWorkflow,
                GeminiSwarmWorkflow,
            ],
            functions=[],
            options=ServiceOptions(
                max_concurrent_workflow_runs=1000,
            ),
        ),
        client.start_service(
            task_queue="tools",
            functions=[get_current_temperature, get_humidity, get_air_quality],
            options=ServiceOptions(
                rate_limit=10,
                max_concurrent_function_runs=10,
                endpoints=False,
            ),
        ),
        client.start_service(
            task_queue="gemini",
            functions=[
                gemini_generate_content,
                gemini_function_call,
                gemini_multi_function_call,
                gemini_multi_function_call_advanced,
            ],
            options=ServiceOptions(
                rate_limit=0.16,
                max_concurrent_function_runs=1,
                endpoints=False,
            ),
        ),
    )


def run_services() -> None:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Service interrupted by user. Exiting gracefully.")


def watch_services() -> None:
    watch_path = Path.cwd()
    logging.info("Watching %s and its subdirectories for changes...", watch_path)
    webbrowser.open("http://localhost:5233")
    run_process(watch_path, recursive=True, target=run_services)


if __name__ == "__main__":
    run_services()
