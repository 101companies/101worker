include ../Makefile.vars
repo = ${resultsdir}/101repo
matches = ${resultsdir}/101meta/matches.json
geshi = ${resultsdir}/geshi
contributions = ${webdir}/contributions

run: ${repo} ${matches} ${geshi} ${contributions}
	@./program.py ${geshi}/run.php

${contributions}:
	mkdir -p ${contributions}

# Remove local temporary files, if any
clean:	
	@#no-op

# Remove files created by this module
reset:
	@find ${contributions} -name "*.geshi.html" -exec rm -f {} \;

# Complete local run by presupposed runs
run-all:
	cd ../match101meta; make run-all
	make run
