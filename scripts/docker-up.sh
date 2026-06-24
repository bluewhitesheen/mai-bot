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

echo "==> Building Docker image (no cache)"
docker compose build --no-cache

echo "==> Starting container in detached mode"
docker compose up -d

echo "==> Done. Check status:"
docker compose ps
