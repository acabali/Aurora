#!/usr/bin/env bash
set -e
MODULE="${MODULE:-main:app}"
exec uvicorn "$MODULE" --host 0.0.0.0 --port "${PORT:-8080}"
