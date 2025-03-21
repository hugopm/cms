#!/usr/bin/env bash
set -x

docker compose -p cmsdev -f docker-compose.dev.yml run  --build --rm --service-ports devcms
