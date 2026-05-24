#!/usr/bin/env sh
set -eu

if [ "${V2_RUN_MIGRATIONS:-0}" = "1" ]; then
  echo "Running V2 database migrations..."
  .venv/bin/alembic upgrade head 2>/dev/null || alembic upgrade head
fi

if [ "${V2_SEED_DATABASE:-0}" = "1" ]; then
  echo "Seeding V2 database..."
  .venv/bin/python scripts/v2_seed_db.py 2>/dev/null || python scripts/v2_seed_db.py
fi

exec uvicorn backend.main:app --host 0.0.0.0 --port "${PORT:-8000}"
