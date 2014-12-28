run:
	python incremental.py

test:
	PYTHONPATH="$$PYTHONPATH:`pwd`" prove --ext=.t.py --exec=python

clean:
	rm -rf TEST

install:
	pip install --upgrade git+https://github.com/rjbs/PyTAP.git

.PHONY: run test clean install
