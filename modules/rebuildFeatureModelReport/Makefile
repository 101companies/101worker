include ../Makefile.vars

run:
	@echo 'Building and cleaning...'
	@make javac
	@make clean-deployment
	@echo 'Creating reports...'
	@python createReport.py ${dumpsDir}/claferFeaturesFlat.json ${dumpsDir}/features.clf ${contrDir}/fileindex.json ${webdir}/data/dumps/ featureModelReports/
	@make clean

javac:
	@mkdir -p bin
	@javac -d bin -sourcepath java-src -cp lib/alloy/alloy4.jar java-src/org/softlang/clafer/SimpleSatChecker.java

clean-deployment:
	@mkdir -p ${webdir}/data/dumps/featureModelReports/
	@rm -rf ${webdir}/data/dumps/featureModelReports/*

clean:
	@rm -rf bin
	@rm -f tmp*
	@rm -f *.pyc



