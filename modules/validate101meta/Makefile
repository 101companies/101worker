include ../Makefile.vars

run: ${pulled101RepoDir} ${dumpsDir} ${contrDir} ${matchesDump}
	@./program.py
	@test -e ${validatorDump}

# Remove local temporary files, if any
clean:	
	@#no-op

# Remove files created by this module
reset:
	@rm -f ${validatorDump}
	@find ${contrDir} -name "*.validator.json" -exec rm -f {} \;
