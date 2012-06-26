include ../Makefile.vars
repo = ${resultsdir}/101repo
result = ${resultsdir}/101meta

run: ${repo} ${result}
	@make clean
	@python program.py ${repo} ${result}

${result}:
	mkdir ${result}

# Remove local temporary files if any
clean:	
	@#no-op

# Complete local run by presupposed runs
run-all:
	@cd ../pull101repo; make
	make run
