#!/usr/bin/env bash

PORT=${PORT:-8082}

exec uvicorn farmer:app --reload --port "$PORT"
