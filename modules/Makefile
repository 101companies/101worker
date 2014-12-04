# Invoke runner and cleaner per module

%.run:
	mkdir -p ../../101results/depend
	../tools/depend ../configs/$*.json  >../../101results/depend/depend.yml
	../tools/runner                      ../../101results/depend/depend.yml

%.debug:
	python ../tools/runner.py $*.json verbose

%.archive:
	python ../tools/archiver.py $*.json
