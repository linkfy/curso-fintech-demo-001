# Variables
UV = uv 
RUN = $(UV) run 
PYTHON = $(RUN) python
# Firma de los comandos
.PHONY: install format format-check lint lint-fix typecheck test check clean docs docs-build

install:
	$(UV) sync

format:
	$(RUN) ruff format .

format-check:
	$(RUN) ruff format . --check 

lint:
	$(RUN) ruff check .

lint-fix:
	$(RUN) ruff check . --fix

typecheck:
	$(RUN) mypy --strict src/

test:
	$(RUN) pytest --cov=src --cov-report=term-missing tests/

docs:
	@echo "Lanzando servidor de documentación http://127.0.0.1:8000"
	$(RUN) mkdocs serve

docs-build:
	@echo "Verificando que la documentación se contruye sin errores..."
	$(RUN) mkdocs build --strict

check: format lint typecheck test docs-build

clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(dir, ignore_errors=True) for dir in \
	 ['.pytest_cache' , '.mypy_cache', '.ruff_cache', '.coverage', 'htmlcov']]"
