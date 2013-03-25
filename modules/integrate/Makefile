include ../Makefile.vars
integrateDir = ${resultsdir}/repos/101integrate

run:
	make clean
	cd ${integrateDir} ; make download-books; make bootstrap; make mine; make from-cache; make analyze; make backlink
	make integrate
	make deploy

integrate:
	cd ${integrateDir} ; make coverageTables	

deploy:
	mkdir -p ${integrateDir}
	cp data/allbooks ${integrateDir}/allbooks
	cp data/perbook ${integrateDir}/perbook

# Remove local temporary files, if any
clean:  
	find ${integrateDir} -type f -delete ;\
	cd ${integrateDir}; make clean

# Remove files created by this module
reset:
	mkdir -p ${modulesDir}/integrate
	make clean
