# Invoke runner and cleaner per module

%.run:
	python ../tools/runner.py $*.config; 

%.debug:
	python ../tools/runner.py $*.config verbose; 

%.archive:
	python ../tools/archiver.py $*.config	
