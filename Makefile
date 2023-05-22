run_uwsgi:
  uwsgi --procname-prefix magnum-api --ini /etc/magnum/magnum-api-uwsgi.ini

run_local:
  python3.8 magnum-api.wsgi.py