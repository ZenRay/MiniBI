#!/usr/bin/env bash
set -euo pipefail

# Usage: ./check_superset_health_login.sh [USERNAME] [PASSWORD] [PROVIDER]
# Defaults: USERNAME=admin PASSWORD=admin PROVIDER=db

HOST="${HOST:-http://localhost:8088}"
USERNAME="${1:-admin}"
PASSWORD="${2:-admin}"
PROVIDER="${3:-db}"
MAX_RETRIES="${MAX_RETRIES:-60}"
SLEEP_SEC="${SLEEP_SEC:-2}"
LOG_DIR="${LOG_DIR:-./logs}"

# Require jq for JSON construction/parsing
if ! command -v jq >/dev/null 2>&1; then
  echo "ERROR: 'jq' is required by this script but not found in PATH."
  echo "Install it (e.g. on Debian/Ubuntu: sudo apt-get install -y jq) and re-run."
  exit 2
fi

# Normalize HOST to include scheme if omitted
if ! echo "$HOST" | grep -qE '^[a-zA-Z]+://'; then
  HOST="http://$HOST"
fi

echo "Checking Superset health at $HOST/health ..."
i=0
until curl -sSf --max-time 5 "$HOST/health" >/dev/null 2>&1; do
  i=$((i+1))
  if [ "$i" -ge "$MAX_RETRIES" ]; then
    echo "Health check failed after $((i*SLEEP_SEC)) seconds."
    exit 1
  fi
  echo "Waiting for /health... ($i/$MAX_RETRIES)"
  sleep "$SLEEP_SEC"
done
echo "Health OK."

# Prepare log dir (but only create on failure)
timestamp() { date +%Y%m%dT%H%M%S; }

on_error() {
  mkdir -p "$LOG_DIR"
  local dir="$LOG_DIR/superset_health_check_$(timestamp)"
  mkdir -p "$dir"
  echo "Collecting debug logs into $dir"
  # save last response body if set
  if [ -n "${BODY-}" ]; then
    printf '%s' "$BODY" > "$dir/response_body.json" || true
  fi
  # docker compose logs for key services
  docker compose logs --no-color --tail=1000 superset > "$dir/superset.log" 2>&1 || true
  docker compose logs --no-color --tail=500 superset-worker > "$dir/superset-worker.log" 2>&1 || true
  docker compose logs --no-color --tail=500 superset-beat > "$dir/superset-beat.log" 2>&1 || true
  docker compose logs --no-color --tail=500 postgres > "$dir/postgres.log" 2>&1 || true
  docker compose logs --no-color --tail=500 redis > "$dir/redis.log" 2>&1 || true
  # docker state
  docker ps -a > "$dir/docker_ps_a.txt" 2>&1 || true
  docker images > "$dir/docker_images.txt" 2>&1 || true
  docker volume ls > "$dir/docker_volumes.txt" 2>&1 || true
  echo "Saved logs to $dir"
}

trap on_error ERR

echo "Attempting login as $USERNAME ..."
# Build JSON payload using jq to ensure correct escaping
PAYLOAD=$(jq -n --arg u "$USERNAME" --arg p "$PASSWORD" --arg prov "$PROVIDER" '{username:$u,password:$p,provider:$prov}')

# Send POST and capture body + HTTP code
RESP_RAW=$(curl -sS -w "\n%{http_code}" -X POST "$HOST/api/v1/security/login" -H "Content-Type: application/json" --data "$PAYLOAD" --max-time 15 || true)
HTTP_CODE=$(echo "$RESP_RAW" | tail -n1)
BODY=$(echo "$RESP_RAW" | sed '$d')

# Save raw body to variable (on_error will persist it)
BODY="$BODY"

if [ "$HTTP_CODE" = "200" ]; then
  # Try to extract access_token with jq (exit non-zero if not present)
  if echo "$BODY" | jq -e '.access_token' >/dev/null 2>&1; then
    ACCESS_TOKEN=$(echo "$BODY" | jq -r '.access_token')
    echo "Login succeeded (HTTP $HTTP_CODE). access_token present. (first 2 lines of response)"
    echo "$BODY" | sed -n '1,2p'
    trap - ERR
    exit 0
  else
    echo "Login response did not contain access_token. Server response (saved to logs on failure):"
    echo "$BODY"
    exit 2
  fi
else
  echo "Login failed (HTTP ${HTTP_CODE:-unknown}). Server response (saved to logs on failure):"
  echo "$BODY"
  exit 2
fi

trap - ERR
