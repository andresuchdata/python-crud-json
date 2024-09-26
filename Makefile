venv:
	python -m venv venv
	@if [ -f venv/Scripts/activate ]; then \
		. venv/Scripts/activate && pip install -r requirements.txt; \
		echo '\nSuccessfully installed project dependencies!'; \
	else \
		chmod +x venv/bin/activate; \
		. venv/bin/activate && pip install -r requirements.txt; \
		echo '\nSuccessfully installed project dependencies!'; \
	fi

run:
	python app.py

.PHONY: venv