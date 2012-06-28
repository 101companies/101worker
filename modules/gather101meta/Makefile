include ../Makefile.defs

run: ${repoDir} ${dumpsDir}
	@./program.py
	@test -e ${rulesDump}

# Remove local temporary files, if any
clean:	
	@#no-op

# Remove files created by this module
reset:
	@rm -f ${rulesDump}

# Complete local run by presupposed runs
run-all:
	@cd ../..; make before-run
	@cd ../pull101repo; make
	make run
