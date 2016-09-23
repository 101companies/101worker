include ../Makefile.vars

run:
	python mongo2Onto.py

test:
	coverage run --source=mongo2Onto.py -m unittest discover
	coverage html

install:
	pip install pymongo
