#!/bin/bash
set -e

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host)
      HOST="$2"
      shift 2
      ;;
    --user)
      USER="$2"
      shift 2
      ;;
    --api-key)
      API_KEY="$2"
      shift 2
      ;;
    --help)
      echo "Usage: $0 [--host HOST] [--user USER] [--api-key DATALAND_API_KEY]"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      echo "Usage: $0 [--host HOST] [--user USER] [--api-key DATALAND_API_KEY]" >&2
      exit 1
      ;;
  esac
done

REMOTE_PATH="/home/${USER}/DatalandMCP"

echo "Deploying DatalandMCP to ${USER}@${HOST}..."

# Create the directory if it doesn't exist
ssh "${USER}@${HOST}" "[ -d ${REMOTE_PATH} ] || mkdir -p ${REMOTE_PATH}"

# Create the .env file
ssh "${USER}@${HOST}" "printf 'DATALAND_API_KEY=${API_KEY}' > ${REMOTE_PATH}/.env"
ssh "${USER}@${HOST}" "chmod 600 ${REMOTE_PATH}/.env"

# Copy the docker-compose.yml file
scp docker-compose.yml "${USER}@${HOST}:${REMOTE_PATH}/docker-compose.yml"

# Change to working directory and start DatalandMCP service
ssh "${USER}@${HOST}" "cd ${REMOTE_PATH} && sudo docker compose --profile mcp up -d"
