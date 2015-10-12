pp = PYTHONPATH="$$PYTHONPATH:$$(dirname $$(pwd))"


doc:
	cd ..; ${pp} pydoc kludge101


test:
	${pp} prove --ext=.t.py -e 'python -W ignore'


cover:
	rm -rf .coverage htmlcov
	for f in t/*.t.py; \
	do \
	    ${pp} coverage run -a --branch --source=. '--omit=t/*.t.py' "$$f"; \
	done;
	coverage html
	@echo See htmlcov/index.html for coverage output.


clean:
	rm -rf .coverage htmlcov


install:
	pip install git+https://github.com/rjbs/PyTAP.git coverage


.PHONY: run clean test install cover doc
