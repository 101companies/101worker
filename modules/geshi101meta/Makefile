include ../Makefile.vars
repo = ${resultsdir}/101repo
geshi = ${resultsdir}/geshi/run.php
result = ${resultsdir}/101meta

run: ${repo} ${geshi} ${result}
	@make clean
	@python program.py ${repo} ${geshi} ${result}

# Remove local temporary files if any
clean:	
	@#no-op

# Remove 101result files created by this module
reset:
	@rm -rf ${result}/geshi
