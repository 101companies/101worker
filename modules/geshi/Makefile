include ../Makefile.vars
repo = ${resultsdir}/101repo
orig = ${repo}/technologies/geshi
result = ${resultsdir}/geshi/src/geshi

run: ${repo} ${orig}
	@make clean
	@cp -r ${orig} ${resultsdir}
	@python program.py ${repo} ${result}

clean:
	@rm -rf ${result}
