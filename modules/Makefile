# Invoke runner and cleaner per module

%.run:
	python ../tools/runner.py $*.json; 

%.debug:
	python ../tools/runner.py $*.json verbose; 

%.archive:
	python ../tools/archiver.py $*.json	
