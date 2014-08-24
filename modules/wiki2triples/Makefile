include ../Makefile.vars
output = ${dumpsDir}/erroneous_pages.json

run:
	./program.py
	cp erroneous_pages.json ${output}

clean:
	rm -f ${output}
	rm -f erroneous_pages.json
