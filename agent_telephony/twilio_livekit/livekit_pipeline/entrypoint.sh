#!/bin/sh
set -e

echo "Running download-files..."
uv run python src/worker.py download-files

echo "Starting livekit worker..."
exec uv run python src/worker.py start