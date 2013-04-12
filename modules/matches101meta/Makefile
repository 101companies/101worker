include ../Makefile.vars

run: ${pulled101RepoDir} ${dumpsDir} ${contrDir} ${rulesDump}
	@#temporarily commented out, replaced by matchesModule.py - which is again already legacy	
	@#@./program.py	
	@./matchesModule.py	
	@test -e ${matchesDump}

# Remove local temporary files, if any
clean:  
	@#no-op

# Remove files created by this module
reset:
	@rm -f ${matchesDump}
	@find ${webdir}/data/resources -name "*.matches.json" -exec rm -f {} \;
