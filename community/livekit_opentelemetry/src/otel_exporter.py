# exporter_setup.py

from opentelemetry.exporter.cloud_monitoring import CloudMonitoringMetricsExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
import os
import atexit
import logging
from opentelemetry import metrics

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingCloudMonitoringMetricsExporter(CloudMonitoringMetricsExporter):
    def export(self, metrics, timeout_millis=None):
        try:
            result = super().export(metrics, timeout_millis=timeout_millis)
            if result is None:  # Assuming None indicates success
                logging.info("Metrics successfully sent to Google Cloud Monitoring.")
            else:
                logging.error("Failed to send metrics to Google Cloud Monitoring.")
            return result
        except Exception as e:
            logging.error(f"Exception during export: {e}")
            return None

def setup_google_cloud_exporter():
    """Set up the Google Cloud exporter."""
    try:
        exporter = LoggingCloudMonitoringMetricsExporter(
            project_id=os.environ.get("GOOGLE_CLOUD_PROJECT")
        )
        logger.info("Google Cloud Monitoring exporter set up successfully.")

        # Set up a periodic exporting metric reader
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)
        logger.info("Periodic exporting metric reader set up successfully.")

        # Ensure the exporter is flushed before the application exits
        atexit.register(reader.shutdown)

        logger.info(f"Using Google Cloud project: {os.environ.get('GOOGLE_CLOUD_PROJECT')}")
        return reader
    except Exception as e:
        logger.error(f"Failed to set up Google Cloud exporter: {e}")
        return None