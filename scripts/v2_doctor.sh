#!/usr/bin/env bash

set -euo pipefail

API_URL="${API_URL:-http://127.0.0.1:8000}"
WEB_URL="${WEB_URL:-http://127.0.0.1:3000}"

check_url() {
  local label="$1"
  local url="$2"

  if curl -fsS "$url" >/dev/null; then
    echo "ok   $label -> $url"
  else
    echo "fail $label -> $url"
    return 1
  fi
}

echo "Checking LEGO Resale Intelligence V2..."
echo ""

check_url "API health" "$API_URL/health"
check_url "API watchlist" "$API_URL/api/watchlist"
check_url "API set intelligence" "$API_URL/api/market/set/75192?days=120"
if curl -fsS -X POST "$API_URL/api/analyze/demo" >/dev/null; then
  echo "ok   API demo analyze -> $API_URL/api/analyze/demo"
else
  echo "fail API demo analyze -> $API_URL/api/analyze/demo"
  exit 1
fi
check_url "Web market" "$WEB_URL/"
check_url "Web analyze" "$WEB_URL/analyze"
check_url "Web watchlist" "$WEB_URL/watchlist"
check_url "Web sets" "$WEB_URL/sets"
check_url "Web portfolio" "$WEB_URL/portfolio"
check_url "Web briefings" "$WEB_URL/briefings"

echo ""
echo "V2 looks healthy."
