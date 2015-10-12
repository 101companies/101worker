include ../Makefile.vars
output = ${dumpsDir}/erroneous_pages.json

run:
	./program.py
	cp errors.json ${output}

clean:
	rm -f ${output}
	rm -f erroneous_pages.json
