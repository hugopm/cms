#!/usr/bin/env bash
set -x

docker compose -p cmstest -f docker-compose.test.yml run --build --rm testcms
