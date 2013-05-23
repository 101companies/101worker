include ../Makefile.vars

run:
	@make generate
	@make deploy

generate:
	@./program.py ${wikiDump}

deploy:
	@cp *.html *.css ${viewsDir}

clean:
	@rm -f *.html *.json
