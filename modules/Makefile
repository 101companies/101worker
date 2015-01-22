# add 101worker/libraries to PYTHONPATH and run the runner
%.run:
	PYTHONPATH="$$PYTHONPATH:$$(dirname $$(pwd))/libraries" \
	    ../tools/runner/runner <../configs/env/$*.yml

%.archive:
	python ../tools/archiver.py $*.json
