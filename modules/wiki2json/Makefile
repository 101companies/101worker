include ../Makefile.vars
output = ${dumpsDir}/wiki.json

run:
	python wiki2json.py
	#cd src
	#mvn clean compile package
	#@java -classpath target/jsonExtractor-1.0-SNAPSHOT-jar-with-dependencies.jar Main
	cp dump.json ${output}

clean:
	rm -f ${output}

