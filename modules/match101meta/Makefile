include ../Makefile.vars
repo = ${resultsdir}/101repo
result = ${resultsdir}/101meta

run: ${repo} ${result}
	@make clean
	@python program.py ${repo} ${result}

clean:	
	@#no-op
