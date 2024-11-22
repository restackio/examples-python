#!/bin/bash

set -e

# Remove the restack_ai package from the virtual environment
poetry remove restack_ai

# Readd the restack_ai package from the local path
poetry add restack_ai
