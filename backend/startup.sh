#!/usr/bin/env bash
set -e

echo "Starting backend service..."

# ...any pre-start commands...

exec poetry run uvicorn main:app --host 0.0.0.0 --port 8000
