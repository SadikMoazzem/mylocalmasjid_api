BLACK ?= \033[0;30m
RED ?= \033[0;31m
GREEN ?= \033[0;32m
YELLOW ?= \033[0;33m
BLUE ?= \033[0;34m
PURPLE ?= \033[0;35m
CYAN ?= \033[0;36m
GRAY ?= \033[0;37m
COFF ?= \033[0m

# Mark non-file targets as PHONY
.PHONY: all docker docker-support docker-shell docker-db lint test deps
.EXPORT_ALL_VARIABLES:
.DEFAULT: help
APP_NAME := mylocalmasjid
db_port ?= 5432


#########
# Local #
#########
check:  ## Run static code analysis, checks and license generation
	@printf "$(CYAN)Running static code analysis, checks and license generation$(COFF)\n"
	@poetry run pip-licenses --with-authors -f markdown --output-file reports/licenses.md
	@make lint

lint:  ## lint the code
	@printf "$(CYAN)Auto-formatting$(COFF)\n"
	@poetry run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place mylocalmasjid_api --exclude=migrations
	@poetry run isort mylocalmasjid_api cli.py --skip mylocalmasjid_api/migrations

deps:  ## install dependencies
	@printf "$(CYAN)Updating deps$(COFF)\n"
	@poetry install

local:  ## Run the app locally
	poetry run uvicorn mylocalmasjid_api.app:app --reload

setup-prod:
	poetry export -f requirements.txt --without-hashes > requirements.txt
	# python3 -m pip download PyNaCl --platform manylinux1_x86_64 --no-deps -d  prod-venv/lib/python3.9/site-packages
	# python3 -m pip download cffi --platform manylinux1_x86_64 --no-deps -d  prod-venv/lib/python3.9/site-packages
	# python3 -m pip download bcrypt --platform manylinux1_x86_64 --no-deps -d  prod-venv/lib/python3.9/site-packages
	# python3 -m pip download cryptography --platform manylinux2014_x86_64 --no-deps -d  prod-venv/lib/python3.9/site-packages
	python3 -m pip install -r requirements.txt -t prod-venv/lib/python3.9/site-packages
	cd prod-venv/lib/python3.9/site-packages && zip -r9 ../../../../lambda.zip .
	zip -g lambda.zip -r mylocalmasjid_api

build:
	rm lambda.zip || true
	poetry build
	poetry run pip install --upgrade -t package dist/mylocalmasjid_api-0.1.0-py3-none-any.whl
	cd package
	zip -r ../lambda.zip . -x '*.pyc'
	# python3 -m pip install --platform=manylinux1_x86_64 --only-binary=:all: psycopg2-binary==2.8.6 -t prod-venv/lib/python3.9/site-packages
	# python3 -m pip install --platform=manylinux1_x86_64 --only-binary=:all: pydantic==1.8.2 -t prod-venv/lib/python3.9/site-packages
