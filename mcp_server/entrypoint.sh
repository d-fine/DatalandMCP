#!/bin/bash
set -e

# Substitute environment variable into mcp.json
echo "Substituting DATALAND_API_KEY into mcp.json..."
if [ -z "$DATALAND_API_KEY" ]; then
    echo "Error: DATALAND_API_KEY environment variable is not set"
    exit 1
fi

# Replace placeholder with actual API key
sed -i "s/PLACEHOLDER_DATALAND_API_KEY/${DATALAND_API_KEY}/g" mcp.json

# Always generate API clients to ensure we have the latest API definitions
echo "Generating Dataland API clients..."
./bin/generate_dataland_api_clients.sh
echo "Installing dependencies..."
pdm install --prod


echo "Starting up DatalandMCP..."
source .venv/bin/activate

echo "Launching MCP Server via streamable-http & MCPO..."
exec python src/mcp_server.py --transport="streamable-http" &
exec mcpo --config mcp.json --port 8000 --host 0.0.0.0

wait