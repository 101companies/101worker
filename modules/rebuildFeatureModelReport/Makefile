include ../Makefile.vars

run:
	@make build
	@python createReport.py ${contrDir}/fileindex.json ${webdir}/data/dumps/featureModelReport.json
	@make clean

build:
	@mkdir -p bin
	@javac -d bin -sourcepath java-src -cp lib/alloy/alloy4.jar java-src/org/softlang/clafer/SimpleSatChecker.java

clean:
	@rm -rf bin
	@rm -f tmp*
	@rm -f *.pyc


