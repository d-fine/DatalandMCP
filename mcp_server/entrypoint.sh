#!/bin/bash
set -e

echo "Checking for README.md:"
if [ -f "README.md" ]; then
    echo "README.md EXISTS in $(pwd)"
    echo "File size: $(stat -c%s README.md) bytes"
    echo "First 10 lines of README.md:"
    head -10 README.md
else
    echo "README.md DOES NOT EXIST in $(pwd)"
fi

if [ -f "/app/README.md" ]; then
    echo "/app/README.md EXISTS"
    echo "File size: $(stat -c%s /app/README.md) bytes"
    echo "First 10 lines of /app/README.md:"
    head -10 /app/README.md
else
    echo "/app/README.md DOES NOT EXIST"
fi

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


echo "Connect to container to start up MCPO..."
source .venv/bin/activate
exec mcpo --config mcp.json --port 8000 --host 0.0.0.0