include ../Makefile.vars

run:
	python genLinkedData.py

test:
	coverage run --source=genLinkedData.py -m unittest discover
	coverage html

install:
	pip install pymongo
