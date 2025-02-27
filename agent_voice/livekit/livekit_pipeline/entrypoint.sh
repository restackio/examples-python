#!/bin/sh
set -e

echo "Running download-files..."
uv run python src/pipeline.py download-files

echo "Starting pipeline..."
exec uv run python src/pipeline.py start