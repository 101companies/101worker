test:
	PYTHONPATH="$$PYTHONPATH:$$(dirname $$(pwd))" prove -v --ext=.t.py -e python

install:
	pip install --upgrade git+https://github.com/rjbs/PyTAP.git

.PHONY: run test install
