include ../Makefile.vars
wiki = ${webdir}/data/dumps/Wiki101Full.json

run:
	@make clean
	@make generate

reset:
	@make clean

generate:
	@./program.py ${wiki}

clean:
	@rm -rf ${pulled101RepoDir}/vocabularies/*
