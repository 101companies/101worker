include ../Makefile.vars
output = ${ontoDir}

all:
	make run

run:
    mkdir -p ${dumpsDir}/sparql_queries
	cp -r specs ${dumpsDir}/sparql_queries/specs
	python runner.py
	mv output ${dumpsDir}/sparql_queries

# Remove local temporary files, if any
clean:
	@#no-op

# Remove files created by this module
reset:
	@#no-op
