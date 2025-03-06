install:
	pip install -r requirements.txt  # Install dependencies.

lint:
	pylint *.py  # Lint code.

run:
	python main.py  # Start app.
