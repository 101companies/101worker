pp = PYTHONPATH="$$PYTHONPATH:$$(dirname $$(pwd))"

test:
	${pp} prove --ext=.t.py -e python
	rm -rf TEST

cover:
	rm -rf .coverage htmlcov
	for f in t/*.t.py; \
	do \
	    ${pp} coverage run -a --branch --source=. '--omit=t/*' "$$f"; \
	done;
	coverage html
	@echo See htmlcov/index.html for coverage output.

clean:
	rm -rf TEST .coverage htmlcov

install:
	pip install --upgrade git+https://github.com/rjbs/PyTAP.git coverage

.PHONY: run test clean install cover
