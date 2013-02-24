include ../Makefile.vars

run: ${pulled101RepoDir} ${dumpsDir} ${contrDir} ${rulesDump}
	@./program.py
	@test -e ${matchesDump}

# Remove local temporary files, if any
clean:  
	@#no-op

# Remove files created by this module
reset:
	@rm -f ${matchesDump}
	@find ${contrDir} -name "*.matches.json" -exec rm -f {} \;
