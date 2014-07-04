include ../Makefile.vars
output = ${ontoDir}

all:
	make run

run:
	cp -r models ${output}
	python pysesame.py
	mv subtyping_errors.json ${dumpsDir}

# Remove local temporary files, if any
clean:
	@#no-op

# Remove files created by this module
reset:
	@#no-op
