include ../Makefile.vars
output = ${dumps101dir}/wiki.json

run:
	curl http://101companies.org/wiki.json -o dump.json
	cp dump.json ${output}

clean:
	rm -f ${output}

install:
	pip install pymongo
