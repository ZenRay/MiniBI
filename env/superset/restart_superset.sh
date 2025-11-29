#!/usr/bin/env bash
set -euo pipefail

# Prefer the newer `docker compose` plugin, fall back to legacy `docker-compose`.
# Store as an array so multi-word commands are executed correctly.
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD=(docker-compose)
else
  echo "ERROR: neither 'docker compose' nor 'docker-compose' found in PATH." >&2
  exit 1
fi

# Ensure script runs from its directory (so relative compose files work)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker is not installed or not in PATH." >&2
  exit 1
fi

echo "Building Superset-related images (this may take a while)..."
"${COMPOSE_CMD[@]}" build --pull --no-cache --build-arg CONTAINER_UID=$(id -u) --build-arg CONTAINER_GID=$(id -g) superset superset-worker superset-beat superset-init

echo "Starting services in detached mode..."
"${COMPOSE_CMD[@]}" up -d

on_error() {
  echo "\n*** ERROR: Superset restart failed. Showing current compose ps and recent logs for debugging: ***\n" >&2
  "${COMPOSE_CMD[@]}" ps || true
  echo "--- superset logs (tail 200) ---"
  "${COMPOSE_CMD[@]}" logs --no-color --tail=200 superset || true
}
trap on_error ERR

echo "Running superset-init (migrations, admin setup, roles sync)..."
echo "Running database migrations (superset db upgrade)..."
"${COMPOSE_CMD[@]}" run --rm superset-init superset db upgrade

echo "Running superset init (sync roles, permissions and default configs)..."
"${COMPOSE_CMD[@]}" run --rm superset-init superset init


# Optional: create admin user from .env if ADMIN_USERNAME and ADMIN_PASSWORD are set.
# We do this defensively: only create if user does not already exist. To force an overwrite
# you'd need to run an explicit reset command (safer to do manually or via CI secrets).
ENV_FILE="$SCRIPT_DIR/.env"
if [ -f "$ENV_FILE" ]; then
  # Read values (strip possible quotes and CR)
  ADMIN_USERNAME=$(grep -E '^ADMIN_USERNAME=' "$ENV_FILE" | sed -E 's/^ADMIN_USERNAME=//;s/^"//;s/"$//;s/\r$//') || ADMIN_USERNAME=""
  ADMIN_PASSWORD=$(grep -E '^ADMIN_PASSWORD=' "$ENV_FILE" | sed -E 's/^ADMIN_PASSWORD=//;s/^"//;s/"$//;s/\r$//') || ADMIN_PASSWORD=""
  ADMIN_EMAIL=$(grep -E '^ADMIN_EMAIL=' "$ENV_FILE" | sed -E 's/^ADMIN_EMAIL=//;s/^"//;s/"$//;s/\r$//') || ADMIN_EMAIL=""
else
  ADMIN_USERNAME=""
  ADMIN_PASSWORD=""
  ADMIN_EMAIL=""
fi

if [ -n "${ADMIN_USERNAME:-}" ] && [ -n "${ADMIN_PASSWORD:-}" ]; then
  echo "Admin credentials found in .env (username=${ADMIN_USERNAME}). Checking if user exists..."
  # Check existence via Postgres query; quiet on errors
  set +e
  EXISTS=$("${COMPOSE_CMD[@]}" exec -T postgres psql -U "${POSTGRES_USER:-superset}" -d "${POSTGRES_DB:-superset}" -tAc "select 1 from ab_user where username='${ADMIN_USERNAME}' limit 1;" 2>/dev/null || true)
  set -e
  if echo "${EXISTS}" | grep -q 1; then
    echo "User '${ADMIN_USERNAME}' already exists; skipping create-admin. To change password, run a manual reset." 
  else
    echo "Creating admin user '${ADMIN_USERNAME}' from .env..."
    # Some docker compose implementations do not accept --env-file for `run`.
    # Export .env into the current shell so compose interpolation picks up values
    # (compose will substitute ${VAR} in the service env when starting the container).
    set -a
    # shellcheck disable=SC1090
    [ -f "$ENV_FILE" ] && . "$ENV_FILE"
    set +a
    "${COMPOSE_CMD[@]}" run --rm superset-init \
      superset fab create-admin --username "$ADMIN_USERNAME" \
      --firstname Admin --lastname User --email "${ADMIN_EMAIL:-admin@example.com}" --password "$ADMIN_PASSWORD"
  fi
fi

trap - ERR
echo "Superset restart + init complete."
