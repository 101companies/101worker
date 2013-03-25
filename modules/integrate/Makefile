include ../Makefile.vars
integrateDir = ${resultsdir}/repos/101integrate

run:
	cd ${integrateDir} ; make download-books; make bootstrap; make mine; make analyze

# Remove local temporary files, if any
clean:  
	@#no-op

# Remove files created by this module
reset:
	@rm -f ${predicatesDump}
	@find ${contrDir} -name "*.predicates.json" -exec rm -f {} \;
