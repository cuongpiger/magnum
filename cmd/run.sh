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

stop_magnum_conductor() {
  echo "Stopping Magnum-Conductor"
  sudo systemctl stop devstack@magnum-cond.service
}

if [ "$1" = "start-api" ]; then
  run_magnum_api
elif [ "$1" = "start-api-uwsgi" ]; then
  run_magnum_api_uwsgi
elif [ "$1" = "stop-api-uwsgi" ]; then
  stop_magnum_api_uwsgi
elif [ "$1" = "flog-api-uwsgi" ]; then
  flog_magnum_api
elif [ "$1" = "stop-conductor" ]; then
  stop_magnum_conductor
elif [ "$1" = "start-conductor" ]; then
  magnum-conductor
else
  echo "Usage: $0 api"
  exit 1
fi
