
load-db-data:
	# Load data from db to create some files
	# get_data_from_file.py True -> to decompress data of db
	# get_data_from_file.py False -> to compress data from db and store 
	../../venv/bin/python3 get_data_from_db.py $(decompress)

mock-db-location:
	# Create and point init.ini to mock db location.
	# Create constants required for testing.
	../../venv/bin/python3 mock_dsl_config.py True
	mkdir -p $(HOME)/.calm/mock/.local/.tests/keys
	mkdir -p $(HOME)/.calm/mock/.local/.tests/runbook_tests
	cp config_test.json $(HOME)/.calm/mock/.local/.tests/config.json
	sh create_constants.sh

mock-db:
	# Load current data to db
	# mock_dsl_db.py True -> to initialize mock db
	# mock_dsl_db.py False -> to use existing db in cache
	../../venv/bin/python3 mock_dsl_db.py True
