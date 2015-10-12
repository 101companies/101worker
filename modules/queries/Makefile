include ../Makefile.vars
output = ${ontoDir}

run:
	rm -rf output
	mkdir -p output
	rm -rf ${dumpsDir}/sparql_queries
	mkdir -p ${dumpsDir}/sparql_queries
	cp -r templates ${dumpsDir}/sparql_queries
	cp -r sparql ${dumpsDir}/sparql_queries
	python runner.py
	cp -r output ${dumpsDir}/sparql_queries

%.run:
	python runner.py $*.sparql

# Remove local temporary files, if any
clean:
	@#no-op

# Remove files created by this module
reset:
	mkdir -p ${dumpsDir}/sparql_queries
