include ../Makefile.vars
output = ${ontoDir}

all:
	mkdir -p output
	mkdir -p ${dumpsDir}/sparql_queries
	make run

run:
	cp -r specs ${dumpsDir}/sparql_queries
	cp -r templates ${dumpsDir}/sparql_queries
	cp -r sparql ${dumpsDir}/sparql_queries
	python runner.py
	cp -r output ${dumpsDir}/sparql_queries

# Remove local temporary files, if any
clean:
	@#no-op

# Remove files created by this module
reset:
	mkdir -p ${dumpsDir}/sparql_queries
