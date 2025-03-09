# otel_setup.py

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from livekit.agents.metrics.base import AgentMetrics, PipelineLLMMetrics, PipelineSTTMetrics, PipelineTTSMetrics, PipelineVADMetrics
import logging
from src.otel_exporter import setup_google_cloud_exporter
from opentelemetry.sdk.resources import Resource
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up the meter provider with the exporter
reader = setup_google_cloud_exporter()
if reader:
    metrics.set_meter_provider(MeterProvider(
        metric_readers=[reader],
        resource=Resource.create({
            "service.name": "livekit_metrics",
            "service.namespace": "livekit_telemetry",
            "service.instance.id": "livekit_pipeline",
        })
    ))
    logger.info("MeterProvider set up successfully with the MetricReader.")
else:
    logger.error("Failed to set up the metric reader with the exporter.")

# Create a meter
meter = metrics.get_meter(__name__)

# Create ValueRecorder instruments for detailed metrics
ttft_recorder = meter.create_histogram(
    name="llm_ttft",
    description="Time to first token for LLM",
    unit="ms",
)

duration_recorder = meter.create_histogram(
    name="llm_duration",
    description="Duration of LLM processing",
    unit="ms",
)

completion_tokens_recorder = meter.create_histogram(
    name="llm_completion_tokens",
    description="Number of completion tokens",
    unit="1",
)

prompt_tokens_recorder = meter.create_histogram(
    name="llm_prompt_tokens",
    description="Number of prompt tokens",
    unit="1",
)

total_tokens_recorder = meter.create_histogram(
    name="llm_total_tokens",
    description="Total number of tokens",
    unit="1",
)

tokens_per_second_recorder = meter.create_histogram(
    name="llm_tokens_per_second",
    description="Tokens processed per second",
    unit="tokens/s",
)

stt_duration_recorder = meter.create_histogram(
    name="stt_duration",
    description="Duration of STT processing",
    unit="ms",
)

stt_audio_duration_recorder = meter.create_histogram(
    name="stt_audio_duration",
    description="Audio duration for STT",
    unit="ms",
)

tts_ttfb_recorder = meter.create_histogram(
    name="tts_ttfb",
    description="Time to first byte for TTS",
    unit="ms",
)

tts_duration_recorder = meter.create_histogram(
    name="tts_duration",
    description="Duration of TTS processing",
    unit="ms",
)

tts_audio_duration_recorder = meter.create_histogram(
    name="tts_audio_duration",
    description="Audio duration for TTS",
    unit="ms",
)

vad_idle_time_recorder = meter.create_histogram(
    name="vad_idle_time",
    description="Idle time for VAD",
    unit="ms",
)

vad_inference_duration_recorder = meter.create_histogram(
    name="vad_inference_duration",
    description="Total inference duration for VAD",
    unit="ms",
)

# Function to record metrics
def record_metrics(agent_metrics: AgentMetrics):
    """Record detailed metrics based on the type of AgentMetrics."""
    if isinstance(agent_metrics, PipelineLLMMetrics):
        ttft_recorder.record(agent_metrics.ttft * 1000, {"label": agent_metrics.label})
        duration_recorder.record(agent_metrics.duration * 1000, {"label": agent_metrics.label})
        completion_tokens_recorder.record(agent_metrics.completion_tokens, {"label": agent_metrics.label})
        prompt_tokens_recorder.record(agent_metrics.prompt_tokens, {"label": agent_metrics.label})
        total_tokens_recorder.record(agent_metrics.total_tokens, {"label": agent_metrics.label})
        tokens_per_second_recorder.record(agent_metrics.tokens_per_second, {"label": agent_metrics.label})
    elif isinstance(agent_metrics, PipelineSTTMetrics):

        stt_duration_recorder.record(agent_metrics.duration * 1000, {"label": agent_metrics.label})
        stt_audio_duration_recorder.record(agent_metrics.audio_duration * 1000, {"label": agent_metrics.label})
    elif isinstance(agent_metrics, PipelineTTSMetrics):

        tts_ttfb_recorder.record(agent_metrics.ttfb * 1000, {"label": agent_metrics.label})
        tts_duration_recorder.record(agent_metrics.duration * 1000, {"label": agent_metrics.label})
        tts_audio_duration_recorder.record(agent_metrics.audio_duration * 1000, {"label": agent_metrics.label})
    elif isinstance(agent_metrics, PipelineVADMetrics):

        vad_idle_time_recorder.record(agent_metrics.idle_time * 1000, {"label": agent_metrics.label})
        vad_inference_duration_recorder.record(agent_metrics.inference_duration_total * 1000, {"label": agent_metrics.label})

def calculate_total_latency(eou_metrics, llm_metrics, tts_metrics):
    """Calculate the total latency."""
    return (
        eou_metrics.end_of_utterance_delay +
        llm_metrics.ttft +
        tts_metrics.ttfb
    ) * 1000  # Convert to milliseconds