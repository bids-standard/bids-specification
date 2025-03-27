validate_citation_cff: CITATION.cff
	cffconvert --validate

update_contributors:
	python tools/add_contributors.py
	python tools/print_contributors.py
	yarn all-contributors generate

.PHONY: runprettier
runprettier:
	prettier --write "src/schema/**/*.yaml"
	python3 -m yamllint -f standard src/schema/ -c .yamllint.yml

.PHONY: commitschema
SCHEMA_CHANGES := $(shell git diff --name-only | grep src/schema/*.yaml)
commitschema:
	@echo SCHEMA_CHANGES $(SCHEMA_CHANGES)
	git add src/schema/*.yaml && \
	git commit -m "[git-blame-ignore-rev] prettified schema files." && \
	git log --grep "\[git-blame-ignore-rev\]" --pretty=format:"# %ai - %ae - %s%n%H" >> .git-blame-ignore-revs \
	|| true

formatschema: runprettier commitschema

# check style of all markdown files
node_modules: npm-requirements.txt
	npm install `cat npm-requirements.txt`

remark: node_modules
	npx remark src/**/*.md --frail --rc-path .remarkrc
