include ../Makefile.defs

run: ${repoDir} ${dumpsDir} ${matchesDump}
	@./program.py
	@test -e ${summaryDump}

# Remove local temporary files, if any
clean:	
	@#no-op

# Remove 101results files created by this module
reset:
	@rm -f ${summaryDump}

# Complete local run by presupposed runs
run-all:
	cd ../match101meta; make run-all
	make run
