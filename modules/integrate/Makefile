include ../Makefile.vars
integrateDir = ${resultsdir}/repos/101integrate

run:
	make clean
	cd ${integrateDir} ; make download-books; make bootstrap; make mine; make from-cache;
	make integrate
	make deploy

integrate:
	cd ${integrateDir}/src/integrate; make coverageTables	

deploy:
	mkdir -p ${webdir}/modules/integrate
	rm -r *.* ${webdir}/modules/integrate/
	cp data/allbooks ${webdir}/modules/integrate/allbooks
	cp data/perbook ${webdir}/modules/integrate/perbook

# Remove local temporary files, if any
clean:  
	cd ${integrateDir} ; make clean

# Remove files created by this module
reset:
	mkdir -f ${webdir}/modules/integrate
	rm -r *.* ${webdir}/modules/integrate/
