#!/usr/bin/env bash
# Manually restore the previous working image (or a specific tag).
#   Usage: rollback.sh            -> redeploys the image that was live before the current one
#          rollback.sh <image:tag> -> redeploys that exact image
set -euo pipefail
STATE_DIR="${STATE_DIR:-$HOME/.cypher-deploy}"
TARGET="${1:-$(cat "$STATE_DIR/previous_image" 2>/dev/null || true)}"
if [[ -z "$TARGET" ]]; then
  echo "No previous image recorded. Pass one explicitly: rollback.sh <image:tag>"
  echo "List available tags: aws ecr list-images --repository-name cypher"
  exit 1
fi
echo "[rollback] redeploying $TARGET"
exec "$(dirname "$0")/deploy.sh" "$TARGET"
