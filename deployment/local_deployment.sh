#!/usr/bin/env bash
set -euo pipefail

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --help)
      echo "Usage: $0 --profile (mcp or all)"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Usage: $0 --profile (mcp or all)"
      exit 1
      ;;
  esac
done

BRANCH=$(git rev-parse --abbrev-ref HEAD)
TAG=$(git rev-parse origin/${BRANCH})

echo "Using image tag ${TAG}"
export DATALAND_MCP_TAG=${TAG}

docker compose --profile ${PROFILE} up -d
