#!/usr/bin/env bash
set -euo pipefail

COMPOSE_CMD="docker compose"

# Ensure script runs from its directory (so relative compose files work)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v docker >/dev/null 2>&1; then
	echo "ERROR: docker is not installed or not in PATH." >&2
	exit 1
fi

echo "Building Superset-related images (this may take a while)..."
"$COMPOSE_CMD" build --pull --no-cache --build-arg CONTAINER_UID=$(id -u) --build-arg CONTAINER_GID=$(id -g) superset superset-worker superset-beat superset-init

echo "Starting services in detached mode..."
"$COMPOSE_CMD" up -d

on_error() {
	echo "\n*** ERROR: Superset restart failed. Showing current compose ps and recent logs for debugging: ***\n" >&2
	"$COMPOSE_CMD" ps || true
	echo "--- superset logs (tail 200) ---"
	"$COMPOSE_CMD" logs --no-color --tail=200 superset || true
}
trap on_error ERR

echo "Running superset-init (migrations, admin setup, roles sync)..."
"$COMPOSE_CMD" run --rm superset-init

trap - ERR
echo "Superset restart + init complete."
