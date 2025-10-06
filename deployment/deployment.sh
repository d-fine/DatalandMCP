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

echo "Deploying DatalandMCP to EC2..."

# Update and install Docker and Docker Compose
ssh -i "$SSH_KEY" "${USER}@${HOST}" "sudo apt update && sudo apt upgrade -y && sudo apt install docker.io docker-compose-plugin -y"

# Pull the latest DatalandMCP image
ssh -i "$SSH_KEY" "${USER}@${HOST}" "sudo docker pull ghcr.io/d-fine/datalandmcp:latest"

# Create the directory if it doesn't exist
ssh -i "$SSH_KEY" "${USER}@${HOST}" "[ -d /home/${USER}/DatalandMCP ] || mkdir -p /home/${USER}/DatalandMCP"

# Secure copy the .env and docker-compose.yml files
scp -i "$SSH_KEY" .env.github "${USER}@${HOST}:/home/${USER}/DatalandMCP/.env"
scp -i "$SSH_KEY" docker-compose.yml "${USER}@${HOST}:/home/${USER}/DatalandMCP/docker-compose.yml"

# Make the .env file readable only by the owner
ssh -i "$SSH_KEY" "${USER}@${HOST}" "chmod 600 /home/${USER}/DatalandMCP/.env"

# Change to working directory and start DatalandMCP service
ssh -i "$SSH_KEY" "${USER}@${HOST}" "cd /home/${USER}/DatalandMCP && sudo docker compose --profile mcp up -d"
