test:
	PYTHONPATH="$$PYTHONPATH:$$(dirname $$(pwd))" prove --ext=.t.py -e python
	rm -rf TEST

clean:
	rm -rf TEST

install:
	pip install --upgrade git+https://github.com/rjbs/PyTAP.git

.PHONY: run test clean install
