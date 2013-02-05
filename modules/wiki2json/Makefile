include ../Makefile.vars
output = ${dumpsDir}/Wiki101Full.json

run:
	cd src 
	mvn clean compile package
	@java -classpath target/jsonExtractor-1.0-SNAPSHOT-jar-with-dependencies.jar Main
	cp dump.json ${output}

clean:
	rm -f ${output}

