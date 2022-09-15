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
	