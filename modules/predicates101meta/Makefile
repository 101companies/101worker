include ../Makefile.vars

run: ${pulled101RepoDir} ${dumpsDir} ${contrDir} ${rulesDump}
	@./program.py
	@test -e ${predicatesDump}

# Remove local temporary files, if any
clean:  
	@#no-op

# Remove files created by this module
reset:
	@rm -f ${predicatesDump}
	@find ${contrDir} -name "*.predicates.json" -exec rm -f {} \;
