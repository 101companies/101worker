include ../Makefile.vars
integrateDir = ${resultsdir}/repos/101integrate

run:
	cd ${integrateDir} ; make download-books; make bootstrap; make mine; make from-cache; make analyze; make backlink
	make integrate
	make deploy

integrate:
	cd ${integrateDir} ; make coverageTables	

deploy:
	mkdir -p ${modulesDir}/integrate
	cp data/allbooks ${modulesDir}/integrate/allbooks
	cp data/perbook ${modulesDir}/integrate/perbook

# Remove local temporary files, if any
clean:  
	find ${modulesDir}/integrate -type f -delete ;\
	cd ${modulesDir}/integrate ; make clean

# Remove files created by this module
reset:
	mkdir -p ${modulesDir}/integrate
	find ${modulesDir}/integrate -type f -delete ;\
