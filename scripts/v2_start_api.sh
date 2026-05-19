#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -x ".venv/bin/uvicorn" ]; then
  echo "No encuentro .venv/bin/uvicorn."
  echo "Ejecuta primero: source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

echo "Starting LEGO Resale Intelligence V2 API..."
echo "Open API docs at: http://127.0.0.1:8000/docs"
.venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000
