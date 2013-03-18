include ../Makefile.vars
wiki = ${webdir}/data/dumps/Wiki101Full.json

run:
	@make generate
	@make deploy

generate:
	python program.py ${wiki}

deploy:
	@cp *.html *.css *.js *.json ${viewsDir}

