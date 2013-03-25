include ../Makefile.vars
integrateDir = ${resultsdir}/repos/101integrate

run:
	make clean
	make bootstrap
	cd ${integrateDir} ; make download-books; make bootstrap; make mine; make from-cache; make analyze; make backlink
	make integrate
	make deploy

bootstrap:
	cd ${integrateDir}/src; python bootstrap.py 	

integrate:
	cd ${integrateDir}/src/integrate ; make integrate

deploy:
	mkdir -p ${modulesDir}/integrate ;\
	cp -r ${integrateDir}/data/allbooks ${modulesDir}/integrate/data ;\
	cp -r ${integrateDir}/data/perbook ${modulesDir}/integrate/data ;\
	python deployResources.py ;\
	cp -r ${integrateDir}/data/summary ${modulesDir}/integrate/data

# Remove local temporary files, if any
clean:  
	rm -r ${modulesDir}/integrate
	mkdir -p ${modulesDir}/integrate

# Remove files created by this module
reset:
	rm -r ${modulesDir}/integrate
	mkdir -p ${modulesDir}/integrate
