# Invoke runner and cleaner per module

%.run:
	../tools/runner/runner <../configs/env/pull.yml

%.debug:
	python ../tools/runner.py $*.json verbose

%.archive:
	python ../tools/archiver.py $*.json
