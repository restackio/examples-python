"""Metrics.

Provides functions for handling and sending metrics data from Livekit to Restack.
"""

import asyncio
import json

from livekit.agents import metrics
from livekit.agents.pipeline import VoicePipelineAgent
from src.restack.client import client
from src.utils import logger, track_task


async def send_metrics(
    pipeline_metrics: metrics.AgentMetrics,
    agent_id: str,
    run_id: str,
) -> None:
    """Send metrics data to restack asynchronously.

    Args:
    pipeline_metrics (metrics.AgentMetrics): The metrics data to be sent.
    agent_id (str): The identifier for the agent.
    run_id (str): The current execution run identifier.

    """
    try:
        latencies = []
        if isinstance(
            pipeline_metrics, metrics.PipelineEOUMetrics
        ):
            total_latency = (
                pipeline_metrics.end_of_utterance_delay
            )
            latencies.append(total_latency * 1000)
        elif isinstance(
            pipeline_metrics, metrics.PipelineLLMMetrics
        ):
            total_latency = pipeline_metrics.ttft
            latencies.append(total_latency * 1000)
        elif isinstance(
            pipeline_metrics, metrics.PipelineTTSMetrics
        ):
            total_latency = pipeline_metrics.ttfb
            latencies.append(total_latency * 1000)
        if latencies:
            metrics_latencies = str(
                json.dumps({"latencies": latencies})
            )
            logger.info(
                "Sending pipeline metrics: %s", metrics_latencies
            )
            await client.send_agent_event(
                event_name="pipeline_metrics",
                agent_id=agent_id,
                run_id=run_id,
                event_input={
                    "metrics": pipeline_metrics,
                    "latencies": metrics_latencies,
                },
            )
    except (TypeError, ValueError) as exc:
        logger.exception("Error processing metrics data: %s", exc)
        raise
    except Exception as exc:
        logger.exception(
            "Unexpected error sending pipeline metrics: %s", exc
        )
        raise


def setup_pipeline_metrics(
    pipeline: VoicePipelineAgent,
    agent_id: str,
    run_id: str,
    usage_collector: metrics.UsageCollector,
) -> None:
    """Configure the pipeline to send metrics when they are collected.

    Attaches a callback to the pipeline that logs metrics data and sends it to restack.

    Args:
    pipeline (VoicePipelineAgent): The pipeline instance.
    agent_id (str): The identifier for the agent.
    run_id (str): The current run identifier.
    usage_collector (metrics.UsageCollector): Collector for aggregating usage metrics.

    """

    @pipeline.on("metrics_collected")
    def on_metrics_collected(
        pipeline_metrics: metrics.AgentMetrics,
    ) -> None:
        try:
            metrics.log_metrics(pipeline_metrics)
            track_task(
                asyncio.create_task(
                    send_metrics(
                        pipeline_metrics, agent_id, run_id
                    )
                )
            )
            usage_collector.collect(pipeline_metrics)
        except (TypeError, ValueError) as exc:
            logger.exception(
                "Error processing collected metrics: %s", exc
            )
            raise
        except Exception as exc:
            logger.exception(
                "Unexpected error handling collected metrics: %s",
                exc,
            )
            raise
