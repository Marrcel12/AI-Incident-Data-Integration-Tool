VENV:=venv
activate-venv:
	.\$(VENV)\Scripts\activate

install: activate-venv
	pip install -r requirments.txt

upload_config:
	docker cp YOUR_SRC/definition.json ad7be4fd1e32:/var/www/MISP/app/files/misp-objects/objects/ai-incident

.PHONY: get-data map-data direct-process run-script

# Command to run the CLI for getting data from Google Sheets
get-data:
	$(VENV)/Scripts/python src/cli.py get_data_from_sheet

# Command to map the data to MISP and save it
map-data:
	$(VENV)/Scripts/python src/cli.py map_to_misp

# Command to process directly and create MISP events
direct-process:
	$(VENV)/Scripts/python src/cli.py direct_process

# MAIN Command to run the script.py which also processes and creates MISP events
run-script:
	$(VENV)/Scripts/python src/script.py

# Command to run pytest
run-tests:
	$(VENV)/Scripts/pytest 

# Command to get performance
performance:
	$(VENV)/Scripts/python src/performance.py
lint:
	$(VENV)/Scripts/black src
