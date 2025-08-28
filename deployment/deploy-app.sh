#!/bin/bash
set -euo pipefail

DEPLOY_DIR="/opt/datalandmcp"
GITHUB_REPO="$1"
DATALAND_API_KEY="$2"

echo "🚀 Starting application deployment..."

# Create deployment directory
sudo mkdir -p "$DEPLOY_DIR"
sudo chown "$(whoami)":"$(whoami)" "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

# Clone or pull latest code from GitHub
if [ -d ".git" ]; then
    echo "📥 Pulling latest code..."
    git pull origin main
else
    echo "📥 Cloning repository..."
    git clone "https://github.com/$GITHUB_REPO.git" .
fi

# Create .env file with secrets (restrict permissions)
umask 077
printf "DATALAND_API_KEY=%s\n" "$DATALAND_API_KEY" > .env

# Stop existing containers
echo "⏹️  Stopping existing containers..."
docker compose down || true

# Remove old images to free up space
echo "🧹 Cleaning up old images..."
docker image prune -f || true

# Build and start services
echo "🔨 Building and starting services..."
docker compose up --build -d

echo "✅ Application deployment completed"