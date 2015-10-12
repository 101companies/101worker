include ../Makefile.vars

run: ${pulled101RepoDir} ${dumpsDir} ${contrDir} 
	@./program.py
	@test -e ${suffixesDump}

# Remove local temporary files, if any
clean:	
	@#no-op

# Remove files created by this module
reset:
	@#no-op
