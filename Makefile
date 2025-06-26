.PHONY:  tools/contributors.tsv

validate_citation_cff: CITATION.cff
	cffconvert --validate

update_contributors:
	uv run tools/add_contributors.py
	uv run tools/print_contributors.py
	npx all-contributors-cli generate

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

schemacodedocs_clean:
	uv run --group=doc sphinx-build -M clean tools/schemacode/docs tools/schemacode/docs/_build

schemacodedocs_build: schemacodedocs_clean
	uv run --group=doc sphinx-build -M html tools/schemacode/docs tools/schemacode/docs/_build

schemacodedocs_serve: schemacodedocs_build
	uv run python -m http.server -d tools/schemacode/docs/_build
