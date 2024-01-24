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
	@poetry run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place api --exclude=migrations
	@poetry run isort api cli.py --skip api/migrations

deps:  ## install dependencies
	@printf "$(CYAN)Updating deps$(COFF)\n"
	@poetry install

local:  ## Run the app locally
	poetry run uvicorn api.app:app --reload