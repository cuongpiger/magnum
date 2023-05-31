run-api-uwsgi:
	@./cmd/run.sh start-api-uwsgi

stop-api-uwsgi:
	@./cmd/run.sh stop-api-uwsgi

flog-api-uwsgi:
	@./cmd/run.sh flog-api-uwsgi

run-api:
	@./cmd/run.sh start-api

stop-conductor:
	@./cmd/run.sh stop-conductor

start-conductor:
	@./cmd/run.sh start-conductor
