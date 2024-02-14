# shortcuts
sync:
	poetry install --extras dev_all --sync

update_lock_only:
	poetry update --lock

update: update_lock_only
	poetry install --extras dev_all

check:
	poetry check

requirements:
	poetry export --without-hashes --with dev -f requirements.txt > requirements.txt

.PHONY: sync update_lock_only update check requirements

black-check:
	black --check .

black-fix:
	black .

isort-check:
	isort . --check

isort-fix:
	isort .

ruff-check:
	ruff check .

ruff-fix:
	ruff check . --fix --show-fixes

mypy:
	mypy .

.PHONY: black-check black-fix isort-check isort-fix ruff-check ruff-fix mypy

pre-check-in: black-check ruff-check mypy

pre-check-in-fix: black-fix ruff-fix mypy

.PHONY: pre-check-in pre-check-in-fix

local_screenpy:
	pip uninstall -y screenpy
	pip install -e ~/projects/screenpy

local_requests:
	pip uninstall -y screenpy_requests
	pip install -e ~/projects/screenpy_requests

local_selenium:
	pip uninstall -y screenpy_selenium
	pip install -e ~/projects/screenpy_selenium

.PHONY: local_requests local_screenpy local_selenium
