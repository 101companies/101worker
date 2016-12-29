include ../Makefile.vars

run:
	python mongo2json.py

test:
	coverage run --source=mongo2json.py -m unittest discover
	coverage html

install:
	pip install pymongo
