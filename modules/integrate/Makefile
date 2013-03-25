include ../Makefile.vars
integrateDir = ${resultsdir}/repos/101integrate

run:
	make bootstrap
	cd ${integrateDir} ; make download-books; make bootstrap; make mine; make from-cache; make analyze; make backlink
	make integrate
	make deploy

bootstrap:
	cd ${integrateDir}/src; python bootstrap.py 	

integrate:
	cd ${integrateDir} ; make coverageTables	

deploy:
	mkdir -p ${modulesDir}/integrate ;\
	cp -r ${integrateDir}/data/allbooks ${modulesDir}/integrate/allbooks ;\
	cp -r ${integrateDir}/data/perbook ${modulesDir}/integrate/perbook ;\
	python deployRespurces.py

# Remove local temporary files, if any
clean:  
	find ${modulesDir}/integrate -type f -delete ;\
	cd ${modulesDir}/integrate ; make clean

# Remove files created by this module
reset:
	mkdir -p ${modulesDir}/integrate
	find ${modulesDir}/integrate -type f -delete ;\
