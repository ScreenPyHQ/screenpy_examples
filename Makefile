# shortcuts
sync:
	poetry install --extras dev --sync

update_lock_only:
	poetry update --lock

update: update_lock_only
	poetry install --extras dev

check:
	poetry check

requirements:
	poetry export --without-hashes --with dev -f requirements.txt > requirements.txt

.PHONY: sync update_lock_only update check requirements

black-check:
	black --check .

black:
	black .

isort-check:
	isort . --check

isort:
	isort .

ruff:
	ruff .

ruff-fix:
	ruff . --fix --show-fixes

mypy:
	mypy .

lint: isort-check ruff mypy

.PHONY: black-check black isort-check isort ruff ruff-fix mypy lint 

pre-check-in: black-check lint

pre-check-in-fix: black isort ruff-fix mypy

.PHONY: pre-check-in pre-check-in-fix
