#!/usr/bin/env bash
# Deploy a CYPHER image on this host with health check + automatic rollback.
#   Usage: deploy.sh <full-image-uri:tag>
#   e.g.   deploy.sh 123456789012.dkr.ecr.us-east-1.amazonaws.com/cypher:42-a1b2c3d
# Called by Jenkins after the image has been pushed to ECR.
set -euo pipefail

IMAGE="${1:?usage: deploy.sh <image-uri:tag>}"
NAME="${CONTAINER_NAME:-cypher}"
HOST_PORT="${HOST_PORT:-80}"
APP_PORT="${APP_PORT:-5000}"
APP_ENV="${APP_ENV:-production}"
AWS_REGION="${AWS_REGION:-us-east-1}"
HEALTH_URL="http://127.0.0.1:${HOST_PORT}/health"
STATE_DIR="${STATE_DIR:-$HOME/.cypher-deploy}"
VERSION="${IMAGE##*:}"
REGISTRY="${IMAGE%%/*}"

mkdir -p "$STATE_DIR"

log() { echo "[deploy] $*"; }

start_container() {   # $1 = image, $2 = version label
  docker run -d \
    --name "$NAME" \
    --restart unless-stopped \
    -p "${HOST_PORT}:${APP_PORT}" \
    -e APP_ENV="$APP_ENV" \
    -e APP_VERSION="$2" \
    -e PORT="$APP_PORT" \
    "$1" >/dev/null
}

wait_healthy() {
  for i in $(seq 1 20); do
    if curl -fsS --max-time 3 "$HEALTH_URL" >/dev/null 2>&1; then
      log "health check passed (attempt $i)"
      return 0
    fi
    sleep 3
  done
  return 1
}

log "logging in to ECR ($REGISTRY)"
aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin "$REGISTRY" >/dev/null

log "pulling $IMAGE"
docker pull "$IMAGE" >/dev/null

PREV_IMAGE=""
if docker container inspect "$NAME" >/dev/null 2>&1; then
  PREV_IMAGE="$(docker inspect --format '{{.Config.Image}}' "$NAME")"
  log "current version: $PREV_IMAGE — keeping it as ${NAME}-previous"
  docker rm -f "${NAME}-previous" >/dev/null 2>&1 || true
  docker stop "$NAME" >/dev/null
  docker rename "$NAME" "${NAME}-previous"
fi

log "starting $IMAGE"
if start_container "$IMAGE" "$VERSION" && wait_healthy; then
  docker rm -f "${NAME}-previous" >/dev/null 2>&1 || true
  [[ -n "$PREV_IMAGE" && "$PREV_IMAGE" != "$IMAGE" ]] && echo "$PREV_IMAGE" > "$STATE_DIR/previous_image"
  echo "$IMAGE" > "$STATE_DIR/current_image"
  log "SUCCESS: $IMAGE is live"
  exit 0
fi

log "FAILED: new version is unhealthy"
docker logs --tail 50 "$NAME" 2>&1 || true
docker rm -f "$NAME" >/dev/null 2>&1 || true

if [[ -n "$PREV_IMAGE" ]]; then
  log "rolling back to $PREV_IMAGE"
  docker rename "${NAME}-previous" "$NAME"
  docker start "$NAME" >/dev/null
  wait_healthy && log "rollback OK" || log "WARNING: rollback container is not healthy either"
fi
exit 1
