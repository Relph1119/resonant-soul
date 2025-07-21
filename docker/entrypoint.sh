#!/usr/bin/env bash

set -e

# -----------------------------------------------------------------------------
# Replace env variables in the service_conf.yaml file
# -----------------------------------------------------------------------------
PY=python3

$PY -u web/web_server.py &

wait
