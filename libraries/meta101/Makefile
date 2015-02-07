test:
	PYTHONPATH="$$PYTHONPATH:$$(dirname $$(pwd))" prove --ext=.t.py -e python

clean:
	rm -rf TEST

install:
	pip install --upgrade git+https://github.com/rjbs/PyTAP.git

.PHONY: run clean test install
