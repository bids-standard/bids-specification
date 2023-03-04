.PHONY:  tools/contributors.tsv

validate_citation_cff: CITATION.cff
	cffconvert --validate

update_contributors:
	python tools/add_contributors.py
	python tools/print_contributors.py
	yarn all-contributors generate

runprettier:
	prettier --write "src/schema/**/*.yaml"
	python3 -m yamllint -f standard src/schema/ -c .yamllint.yml

SCHEMA_CHANGES := $(shell git diff --name-only | grep src/schema/*.yaml)

commitschema:
	@echo SCHEMA_CHANGES $(SCHEMA_CHANGES)
	git add src/schema/*.yaml && \
	git commit -m "[git-blame-ignore-rev] prettified schema files." && \
	git log --grep "\[git-blame-ignore-rev\]" --pretty=format:"# %ai - %ae - %s%n%H" >> .git-blame-ignore-revs \
	|| true

formatschema: runprettier commitschema

all:

.PHONY: runprettier commitschema
