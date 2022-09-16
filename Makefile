.PHONY:  tools/contributors.tsv

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

