#!/usr/bin/sh

run_magnum_api() {
  echo "Running Magnum service in LOCAL mode"
  python3.8 magnum-api-wsgi.py
}

run_magnum_api_uwsgi() {
  echo "Running Magnum-API in uWSGI mode"
  uwsgi --procname-prefix magnum-api --ini /etc/magnum/magnum-api-uwsgi.ini
}

flog_magnum_api() {
  echo "Showing Magnum-API log"
  sudo journalctl --unit devstack@magnum-api.service -f
}

stop_magnum_api_uwsgi() {
  echo "Stopping Magnum-API in uWSGI mode"
  sudo systemctl stop devstack@magnum-api.service
}

if [ "$1" = "start-api" ]; then
  run_magnum_api
elif [ "$1" = "start-api-uwsgi" ]; then
  run_magnum_api_uwsgi
elif [ "$1" = "stop-api-uwsgi" ]; then
  stop_magnum_api_uwsgi
elif [ "$1" = "flog-api-uwsgi" ]; then
  flog_magnum_api
else
  echo "Usage: $0 api"
  exit 1
fi
