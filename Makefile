build-dev:
	@echo "Building for DEV"
	@pip install --editable .
	@echo "Done"

run-dev:
	@python main.py --config-file magnum-conf.ini
