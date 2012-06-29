include ../Makefile.vars

run: ${pulled101RepoDir} ${dumpsDir} ${matchesDump}
	@./program.py
	@test -e ${summaryDump}

# Remove local temporary files, if any
clean:	
	@#no-op

# Remove 101results files created by this module
reset:
	@rm -f ${summaryDump}
