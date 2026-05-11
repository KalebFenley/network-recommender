#!/bin/bash
# autodeploy.sh
# Run this script via cron on your home server (e.g. */5 * * * * /path/to/autodeploy.sh)

set -euo pipefail

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
    exit 0
elif [ "$LOCAL" = "$BASE" ]; then
    echo "Changes detected from GitHub (fast-forward). Deploying..."
    git pull --ff-only
else
    # History was rewritten (e.g. git filter-repo / amend / force-push).
    # Since this is a single-maintainer repo, hard-reset to origin is safe.
    echo "WARNING: Local history has diverged from origin (force-push detected)."
    echo "Hard-resetting to origin/master..."
    git reset --hard origin/master
fi

# Rebuild and restart containers with the latest code/YAML files
docker compose up -d --build

# Clean up dangling images
docker image prune -f

echo "Deployment complete."
