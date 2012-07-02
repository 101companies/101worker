include ../Makefile.vars

run: ${pulled101RepoDir} ${dumpsDir}
	@./program.py
	@test -e ${rulesDump}

# Remove local temporary files, if any
clean:	
	@#no-op

# Remove files created by this module
reset:
	@rm -f ${rulesDump}
