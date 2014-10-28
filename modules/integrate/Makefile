include ../Makefile.vars
integrateDir = ${resultsdir}/repos/101integrate
termResourcesDir = ../../services/termResources

run:
	make clean
	make bootstrap
	cd ${integrateDir} ; make download-books; make bootstrap; make mine; make from-cache; make analyze; make backlink
	make integrate
	make deploy

bootstrap:
	mkdir -p ${integrateDir}; cd ${integrateDir}/../ ; git clone https://github.com/101companies/101integrate.git
	cd ${integrateDir}/src; python bootstrap.py 	

integrate:
	cd ${integrateDir}/src/integrate ; make integrate

deploy:
	mkdir -p ${modulesDir}/integrate ;\
	cp -r ${integrateDir}/data/allbooks ${modulesDir}/integrate ;\
	cp -r ${integrateDir}/data/perbook ${modulesDir}/integrate ;\
	python deployResources.py ;\
	cp -r ${integrateDir}/data/summary ${modulesDir}/integrate
	cp ${integrateDir}/data/allbooks/backlinks.json ${termResourcesDir}
	cp ${integrateDir}/data/allbooks/mapping.json ${termResourcesDir}

# Remove local temporary files, if any
clean:  
	rm -rf ${modulesDir}/integrate
	mkdir -p ${modulesDir}/integrate

# Remove files created by this module
reset:
	rm -r ${modulesDir}/integrate
	mkdir -p ${modulesDir}/integrate

#installing und building 101-folder-structure
setup:						#ls for debugging
	mkdir -p ${modulesDir}/integrate
	mkdir -p ${resultsdir}/repos
	cd ${resultsdir}/repos; git clone https://github.com/101companies/101integrate; ls
	cd ${resultsdir}/repos/101integrate; ls; cd src; ls; touch Makefile.vars ; ls # integrateDir undefined if not existens on starting time of this Makefile
	cd ${resultsdir}/repos/101integrate ; make download-deps
