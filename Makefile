build-dev:
	@echo "Building for DEV"
	@pip install --editable .
	@echo "Done"

run-dev:
	@python main.py --config-file magnum-conf.ini

# This section only runs if you ran `make build-dev`
magnum-run-api:
	@echo "Running magnum-api"
	@magnum-api --config-file magnum-conf.ini

