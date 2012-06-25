include ../Makefile.vars
repo = ${resultsdir}/101repo
result = ${resultsdir}/101meta

run: ${repo} ${result}
	@make clean
	@python program.py ${repo} ${result}

${result}:
	mkdir ${result}

clean:	
	@#no-op
