include ../Makefile.vars

run:
	@make generate
	@make deploy

generate:
	python program.py ${wikiDump}

deploy:
	@cp *.html *.css ${viewsDir}
	mkdir -p ${dumpsDir}/moretagclouds
	@cp *.js *.json ${dumpsDir}/moretagclouds

