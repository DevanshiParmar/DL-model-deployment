#!/bin/bash
# deploy.sh - Triggers deployment via Render Webhook

if [ -z "$RENDER_DEPLOY_WEBHOOK" ]; then
  echo "Error: RENDER_DEPLOY_WEBHOOK is not set"
  exit 1
fi

echo "Triggering deployment on Render..."
curl -X POST "$RENDER_DEPLOY_WEBHOOK"

