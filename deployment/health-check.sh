#!/bin/bash
set -euo pipefail

DEPLOY_DIR="/opt/datalandmcp"

cd "$DEPLOY_DIR"

echo "🔍 Waiting for containers to become healthy (max 5 minutes)..."

# Wait for health checks (20 attempts × 15 seconds = 5 minutes)
for i in {1..20}; do
    MCP_STATUS=$(docker compose ps dataland-mcp-server --format "{{.Health}}")
    WEBUI_STATUS=$(docker compose ps open-webui --format "{{.Health}}")
    
    echo "Attempt $i/20 - MCP: $MCP_STATUS, WebUI: $WEBUI_STATUS"
    
    if [[ "$MCP_STATUS" == "healthy" && "$WEBUI_STATUS" == "healthy" ]]; then
        echo "✅ All containers are healthy!"
        docker compose ps
        exit 0
    elif [[ "$MCP_STATUS" == "unhealthy" || "$WEBUI_STATUS" == "unhealthy" ]]; then
        echo "❌ Container health check failed!"
        docker compose ps
        docker compose logs --no-color --tail=200
        exit 1
    fi
    
    sleep 15
done

echo "❌ Health check timeout after 5 minutes"
docker compose ps
exit 1