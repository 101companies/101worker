include ../Makefile.vars

run: ${pulled101RepoDir} ${dumpsDir} ${contrDir} ${matchesDump}
	@./program.py
	@test -e ${fragmentsDump}

# Remove local temporary files, if any
clean:	
	@#no-op

# Remove files created by this module
reset:
	@rm -f ${fragmentsDump}
	@find ${contrDir} -name "*.fragments.json" -exec rm -f {} \;
