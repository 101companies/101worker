include ../Makefile.vars
output = ${ontoDir}

run:
	./rewrite.py
	cp erroneous_pages.json ${output}

all:
	make run

run:
	cp -r models ${output}
	mv subtyping_errors.json ${dumpsDir}

# Remove local temporary files, if any
clean:
	@#no-op

# Remove files created by this module
reset:
	@#no-op
