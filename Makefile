run_uwsgi: uwsgi --procname-prefix magnum-api --ini /etc/magnum/magnum-api-uwsgi.ini

run-magnum-api:
	@./cmd/run.sh api
