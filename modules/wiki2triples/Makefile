include ../Makefile.vars
output = ${dumpsDir}/wikiLinks.json

run:
	./program.py
	cp wikiLinks.json $output

clean:
	rm -f ${output}
	rm -f wikiLinks.json