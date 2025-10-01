#!/bin/bash
set -e

EC2_HOST=${EC2_HOST:-172.20.14.96}
EC2_USER=${EC2_USER:-ubuntu}
SSH_KEY=${SSH_KEY:-~/.ssh/id_ed25519_AWS_MCP}

echo "Deploying DatalandMCP to EC2..."

# Update and install Docker and Docker Compose
ssh -i "$SSH_KEY" "${EC2_USER}@${EC2_HOST}" "sudo apt update && sudo apt upgrade -y && sudo apt install docker.io docker-compose-plugin -y"

# Pull the latest DatalandMCP image
ssh -i "$SSH_KEY" "${EC2_USER}@${EC2_HOST}" "sudo docker pull ghcr.io/d-fine/datalandmcp:latest"

# Create the directory if it doesn't exist
ssh -i "$SSH_KEY" "${EC2_USER}@${EC2_HOST}" "[ -d /home/${EC2_USER}/DatalandMCP ] || mkdir -p /home/${EC2_USER}/DatalandMCP"

# Secure copy the .env and docker-compose.yml files
scp -i "$SSH_KEY" .env.github "${EC2_USER}@${EC2_HOST}:/home/${EC2_USER}/DatalandMCP/.env"
scp -i "$SSH_KEY" docker-compose.yml "${EC2_USER}@${EC2_HOST}:/home/${EC2_USER}/DatalandMCP/docker-compose.yml"

# Make the .env file readable only by the owner
ssh -i "$SSH_KEY" "${EC2_USER}@${EC2_HOST}" "chmod 600 /home/${EC2_USER}/DatalandMCP/.env"

# Change to working directory and start DatalandMCP service
ssh -i "$SSH_KEY" "${EC2_USER}@${EC2_HOST}" "cd /home/${EC2_USER}/DatalandMCP && sudo docker compose --profile mcp up -d"
