build-dev:
	@echo "Building for DEV"
	@pip install --editable .
	@echo "Done"

run-dev:
	@python main.py --config-file magnum-conf.ini

export-packages:
	@echo "Exporting packages"
	@pip list --format=freeze > requirements.txt
	@echo "Done"

# This section only runs if you ran `make build-dev`
magnum-run-api:
	@echo "Running magnum-api"
	@magnum-api --config-file magnum-conf.ini

