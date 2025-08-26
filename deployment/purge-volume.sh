#!/bin/bash
set -euo pipefail

DEPLOY_DIR="/opt/datalandmcp"

cd "$DEPLOY_DIR"

echo "🗑️ Purging Open Web UI volume..."
docker compose down -v || true
docker volume rm datalandmcp_open-webui 2>/dev/null || echo "Volume does not exist or already removed"
echo "✅ Volume purged successfully"