include ../Makefile.vars
output = ${dumps101dir}/wiki.json

run:
	python wiki2json.py
	cp dump.json ${output}

clean:
	rm -f ${output}

install:
	pip install pymongo
