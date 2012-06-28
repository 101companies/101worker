include ../Makefile.defs

run: ${repoDir} ${dumpsDir} ${contrDir} ${rulesDump}
	@./program.py
	@test -e ${matchesDump}

# Remove local temporary files, if any
clean:  
	@#no-op

# Remove files created by this module
reset:
	@rm -f ${matchesDump}

# Complete local run by presupposed runs
run-all:
	cd ../gather101meta; make run-all
	make run
