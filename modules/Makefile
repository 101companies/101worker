# Invoke runner and cleaner per module

%.run:
	../tools/parallel_runner $*.json; 

%.debug:
	python ../tools/runner.py $*.json verbose; 

%.archive:
	python ../tools/archiver.py $*.json	
