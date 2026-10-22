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

# Railway's edge proxy forwards the visitor address in X-Forwarded-For. uvicorn
# only reads that header from these trusted (private) peers, and then takes the
# right-most address that is not one of them, so per-IP rate limits see the real
# visitor and a client cannot spoof it. See README "Public demo hardening".
FORWARDED_ALLOW_IPS="${FORWARDED_ALLOW_IPS:-127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,100.64.0.0/10,fc00::/7}"

exec uvicorn backend.main:app --host 0.0.0.0 --port "${PORT:-8000}" \
  --proxy-headers --forwarded-allow-ips "$FORWARDED_ALLOW_IPS"
