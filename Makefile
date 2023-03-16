# shortcuts
sync:
	poetry install --extras dev --sync

update:
	poetry update --extras dev

requirements:
	poetry export --without-hashes --with dev -f requirements.txt > requirements.txt

.PHONY: sync update requirements
