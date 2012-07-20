include ../Makefile.vars

run: ${pulled101RepoDir} ${dumpsDir} ${contrDir} ${rulesDump}
	@./program.py
	@test -e ${resolutionDump}

# Remove local temporary files, if any
clean:  
	@#no-op

# Remove files created by this module
reset:
	@rm -f ${resolutionDump}
