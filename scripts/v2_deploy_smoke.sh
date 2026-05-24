#!/usr/bin/env sh
set -eu

API_URL="${API_URL:-}"
WEB_URL="${WEB_URL:-}"

if [ -z "$API_URL" ] || [ -z "$WEB_URL" ]; then
  echo "Usage:"
  echo "  API_URL=https://your-railway-api.up.railway.app WEB_URL=https://your-vercel-app.vercel.app sh scripts/v2_deploy_smoke.sh"
  exit 2
fi

echo "Checking deployed LEGO Resale Intelligence V2..."

check_url() {
  label="$1"
  url="$2"
  if curl -fsS "$url" >/dev/null; then
    echo "ok   $label -> $url"
  else
    echo "fail $label -> $url"
    exit 1
  fi
}

check_post() {
  label="$1"
  url="$2"
  if curl -fsS -X POST "$url" >/dev/null; then
    echo "ok   $label -> $url"
  else
    echo "fail $label -> $url"
    exit 1
  fi
}

check_url "API health" "$API_URL/health"
check_url "API data quality" "$API_URL/api/market/data-quality"
check_url "API active evidence" "$API_URL/api/market/active-evidence"
check_post "API demo analyze" "$API_URL/api/analyze/demo"
check_url "Web market" "$WEB_URL/"
check_url "Web analyze" "$WEB_URL/analyze"
check_url "Web research" "$WEB_URL/research"
check_url "Web portfolio" "$WEB_URL/portfolio"

echo
echo "Deployed V2 looks reachable."
