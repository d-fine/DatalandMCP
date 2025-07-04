#!/usr/bin/env bash
if ! grep -q "DatalandMCP" pyproject.toml; then
  echo "Please ensure that you call this script from the root of the python project (i.e., using ./bin/setup_dev_environment.sh)"
  exit 1
fi

CURRENT_PATH=$(realpath "$(pwd)")
if [[ $HOMEDRIVE == "C:" ]]; then
  CURRENT_PATH=$(echo "$CURRENT_PATH" | sed 's/\/c/c:/g')
fi

sed -i '/DATALAND_QARG_ROOT_DIR/d' .env
echo 'DATALAND_QARG_ROOT_DIR="'$CURRENT_PATH'"' >> .env


set -euxo pipefail
mkdir -p "./clients"

# Generate clients
./bin/generate_dataland_api_clients.sh

# Setup PDM
pdm install