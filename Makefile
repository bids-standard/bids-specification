.DEFAULT_GOAL := help

# determines what "make help" will show
define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

################################################################################
#   General

.PHONY: help

help: ## Show what this Makefile can do
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

validate_cff: CITATION.cff
	cffconvert --validate
