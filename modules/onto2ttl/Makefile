include ../Makefile.vars
output = ${ontoDir}

all:
	make run

run:
	python json2ttl.py
	cp -r models ${output}
	cp -r ttl ${output}
	cp config.json ${output}

# Remove local temporary files, if any
clean:
	@#no-op

# Remove files created by this module
reset:
	@#no-op
