include ../Makefile.vars

run:
	@make clean
	@make generate

reset:
	@make clean

generate:
	@python program.py ${wikiDump}

clean:
	@rm -rf ${pulled101RepoDir}/themes/*
