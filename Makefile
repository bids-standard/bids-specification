.PHONY:  tools/contributors.tsv
all:

install: .venv node_modules

node_modules: package.json package-lock.json
	npm install

.venv: pyproject.toml uv.lock
	uv sync --frozen --group doc --group tools

validate_citation_cff: CITATION.cff .venv
	uv run cffconvert --validate

update_contributors: .venv
	uv run tools/add_contributors.py
	uv run tools/print_contributors.py
	npx all-contributors-cli generate

runprettier:
	npx prettier --write "src/schema/**/*.yaml"
	python3 -m yamllint -f standard src/schema/ -c .yamllint.yml

SCHEMA_CHANGES := $(shell git diff --name-only | grep src/schema/*.yaml)

commitschema:
	@echo SCHEMA_CHANGES $(SCHEMA_CHANGES)
	git add src/schema/*.yaml && \
	git commit -m "[git-blame-ignore-rev] prettified schema files." && \
	git log --grep "\[git-blame-ignore-rev\]" --pretty=format:"# %ai - %ae - %s%n%H" >> .git-blame-ignore-revs \
	|| true

formatschema: runprettier commitschema

.PHONY: runprettier commitschema

schemacodedocs_clean:
	uv run --group=doc sphinx-build -M clean tools/schemacode/docs tools/schemacode/docs/_build

schemacodedocs_build: schemacodedocs_clean
	uv run --group=doc sphinx-build -M html tools/schemacode/docs tools/schemacode/docs/_build

schemacodedocs_serve: schemacodedocs_build
	uv run python -m http.server -d tools/schemacode/docs/_build

validateschema:
	uv run bst export > bep-23_schema.json
	../bids-validator/local-run --schema file://${PWD}/bep-23_schema.json ../bids-examples/petprep/ --ignoreWarnings --verbose --ignoreNiftiHeaders -r ; \
	example_status=$$?; 
