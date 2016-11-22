include ../Makefile.vars

run:
	python genLinkedData.py

test:
	coverage run --source=mongo2Onto.py -m unittest discover
	coverage html

install:
	pip install pymongo
