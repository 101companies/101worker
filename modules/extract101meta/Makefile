include ../Makefile.defs

run: ${repoDir} ${dumpsDir} ${contrDir} ${matchesDump}
	@./program.py
	@test -e ${extractorDump}

# Remove local temporary files, if any
clean:	
	@#no-op

# Remove files created by this module
reset:
	@rm -f ${extractorDump}
	@find ${contrDir} -name "*.extractor.json" -exec rm -f {} \;

# Complete local run by presupposed runs
run-all:
	cd ../validate101meta; make run-all
	make run
