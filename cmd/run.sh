#!/usr/bin/sh

run_magnum_api() {
  echo "Running Magnum service at local"
  python3.8 magnum-api-wsgi.py
}

# shellcheck disable=SC2039
if "$1" == "api"; then
  run_magnum_api
else
  echo "Usage: $0 api"
  exit 1
fi
