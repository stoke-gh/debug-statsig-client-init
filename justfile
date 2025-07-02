set shell := ["bash", "-uc"]
set windows-shell := ["sh", "-uc"]

set ignore-comments
set positional-arguments

set dotenv-load
set dotenv-path := ".env"

# Build all python packages.
[working-directory: 'python']
build:
  uv sync --all-extras --all-packages --dev

# Run locally via uv.
[working-directory: 'python']
run-direct:
  uv run repro

# Run via docker.
[working-directory: 'python']
run-docker:
  docker-compose up --build

# Run via tilt.
[working-directory: 'iac']
tilt *args:
  #!/usr/bin/env bash
  set -euo pipefail
  tilt "$@"

# Send a curl to test the endpoint.
test:
  curl "http://localhost:8000/v1/test"
