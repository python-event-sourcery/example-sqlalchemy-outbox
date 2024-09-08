.PHONY: lint
lint:
	ruff format src
	ruff check src --fix
	mypy src/


.PHONY: test
test:
	pytest --cov=src --cov-report=term-missing src/tests.py
