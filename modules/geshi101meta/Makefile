include ../Makefile.vars
repo = ${resultsdir}/101repo
geshi = ${resultsdir}/geshi/run.php
matches = ${resultsdir}/101meta/matches.json
result = ${resultsdir}/101meta

run: ${repo} ${geshi} ${matches} ${result}
	@make clean
	@python program.py ${repo} ${geshi} ${matches} ${result}

# Remove local temporary files if any
clean:	
	@#no-op

# Remove 101results files created by this module
reset:
	@rm -rf ${result}/geshi

# Complete local run by presupposed runs
run-all:
	cd ../match101meta; make run-all
	make run
