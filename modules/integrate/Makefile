include ../Makefile.vars
integrateDir = ${resultsdir}/repos/101integrate

run:
	cd ${integrateDir} ; make download-books; make bootstrap; make mine; 
	make integrate
	make deploy

integrate:
	cd ${integrateDir}/src/integrate; make coverageTables	

deploy:
	mkdir -p ${webdir}/modules/integrate
	rm -r *.* ${webdir}/modules/integrate/

# Remove local temporary files, if any
clean:  
	@#no-op

# Remove files created by this module
reset:
	mkdir -f ${webdir}/modules/integrate
	rm -r *.* ${webdir}/modules/integrate/
