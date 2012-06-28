include ../Makefile.defs

run: ${repoDir} ${dumpsDir} ${contrDir} ${matchesDump}
	@./program.py
	@test -e ${validatorDump}

# Remove local temporary files, if any
clean:	
	@#no-op

# Remove files created by this module
reset:
	@rm -f ${validatorDump}
	@find ${contrDir} -name "*.validator.json" -exec rm -f {} \;

# Complete local run by presupposed runs
run-all:
	cd ../match101meta; make run-all
	make run
