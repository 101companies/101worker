include ../Makefile.vars
output = ${viewsDir}/linked_data/

run:
	cd src 
	mvn clean compile package
	@java -classpath target/demos-1.0-SNAPSHOT-jar-with-dependencies.jar Main
	mkdir -p ${output}
	cp oo.html ${output}
	cp fp.html ${output}

clean:
	rm -f ${output}

