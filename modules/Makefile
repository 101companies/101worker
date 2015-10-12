# For adding 101worker/libraries to PYTHONPATH
pp = PYTHONPATH="$$PYTHONPATH:$$(dirname $$(pwd))/libraries"

%.run:
	${pp} ../tools/runner/runner <../configs/env/$*.yml \
	                             >../../101logs/runner.log 2>&1

%.debug:
	${pp} ../tools/runner/runner <../configs/env/$*.yml
