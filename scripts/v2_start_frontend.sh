#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/../frontend"

if ! command -v npm >/dev/null 2>&1; then
  echo "No encuentro npm."
  echo "Instala Node.js/npm antes de arrancar la web V2."
  exit 1
fi

if [ ! -d "node_modules" ]; then
  echo "No encuentro frontend/node_modules."
  echo "Ejecuta primero: cd frontend && npm install"
  exit 1
fi

echo "Starting LEGO Resale Intelligence V2 web..."
echo "Open web app at: http://127.0.0.1:3000"
npm run dev -- --hostname 127.0.0.1 --port 3000
