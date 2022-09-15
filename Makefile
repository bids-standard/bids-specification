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

.PHONY: help tools/contributors.tsv

help: ## Show what this Makefile can do
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

validate_citation_cff: CITATION.cff
	cffconvert --validate

update_citation_cff:
	python tools/tributors_to_citation.py 

update_readme_all_contrib:
	yarn all-contributors generate

update_all_contributors:
	tributors update allcontrib

tools/contributors.tsv:
	rm -f tools/contributors.tsv
	curl -L "https://docs.google.com/spreadsheets/d/1pYMQvyL_nY2yt2biPFuBjcUeOExq1WXuK67V5sKjseo/export?format=tsv" -o tools/contributors.tsv
	