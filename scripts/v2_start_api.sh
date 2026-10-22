#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -x ".venv/bin/uvicorn" ]; then
  echo "No encuentro .venv/bin/uvicorn."
  echo "Ejecuta primero: source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

# Local development defaults: API docs on, writes allowed, local frontend origins.
# The deployed API (scripts/v2_boot_api.sh) keeps the safe defaults instead.
export LRI_ENABLE_DOCS="${LRI_ENABLE_DOCS:-1}"
export LRI_DEMO_ALLOW_WRITES="${LRI_DEMO_ALLOW_WRITES:-1}"
export BACKEND_CORS_ORIGINS="${BACKEND_CORS_ORIGINS:-http://localhost:3000,http://127.0.0.1:3000}"

echo "Starting LEGO Resale Intelligence V2 API..."
echo "Open API docs at: http://127.0.0.1:8000/docs"
.venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000
