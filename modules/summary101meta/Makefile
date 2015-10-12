include ../Makefile.vars

run: ${pulled101RepoDir} ${dumpsDir} ${contrDir} ${matchesDump} ${predicatesDump} ${fragmentsDump}
	@./program.py
#	@test -e ${summaryDump}

# Remove local temporary files, if any
clean:	
	@#no-op

# Remove files created by this module
reset:
#	@rm -f ${summaryDump}
	@find ${contrDir} -name "*.summary.json" -exec rm -f {} \;
