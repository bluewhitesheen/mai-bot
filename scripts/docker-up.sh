#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: docker not found. Please install Docker first."
  exit 1
fi

if [ ! -f docker-compose.yml ]; then
  echo "Error: docker-compose.yml not found in project root."
  exit 1
fi

if command -v docker-compose >/dev/null 2>&1; then
  COMPOSE=(docker-compose)
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  COMPOSE=(docker compose)
else
  echo "Error: docker compose is not available. Install Docker Compose."
  exit 1
fi

echo "==> Building Docker image (no cache)"
if ! "${COMPOSE[@]}" build --no-cache; then
  echo "Warning: build with --no-cache failed. Retrying with normal cache."
  "${COMPOSE[@]}" build
fi

echo "==> Starting container in detached mode"
"${COMPOSE[@]}" up -d

echo "==> Done. Check status:"
"${COMPOSE[@]}" ps
