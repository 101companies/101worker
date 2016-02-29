include ../Makefile.vars
output = ${dumps101dir}/wiki.json

run:
	python wiki2json.py

clean:
	rm -f ${output}

test:
	coverage run --source=wiki2json.py -m unittest discover
	coverage html

install:
	pip install inflection
