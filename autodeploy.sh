#!/bin/bash
# autodeploy.sh
# Run this script via cron on your home server (e.g. */5 * * * * /path/to/autodeploy.sh)

cd "$(dirname "$0")" || exit

# Fetch latest from origin
git fetch origin

# Check if we are behind master
UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "Up-to-date. No deployment needed."
elif [ "$LOCAL" = "$BASE" ]; then
    echo "Changes detected from GitHub! Deploying..."
    git pull
    
    # We rebuild to ensure the frontend static site compiles the latest updates.
    # The backend will restart and reload the newest YAML files.
    docker compose up -d --build
    
    # Optional cleanup of old dangling images
    docker image prune -f
    
    echo "Deployment complete."
else
    echo "Local repository has diverged. Manual intervention required."
fi
