include ../Makefile.vars
repo = ${resultsdir}/101repo
matches = ${resultsdir}/101meta/matches.json
result = ${resultsdir}/101meta

run: ${repo} ${matches} ${result}
	@make clean
	@python program.py ${repo} ${matches} ${result}

# Remove local temporary files if any
clean:	
	@#no-op

# Remove 101results files created by this module
reset:
	@rm -rf ${result}/validation.json

# Complete local run by presupposed runs
run-all:
	cd ../match101meta; make run-all
	make run
