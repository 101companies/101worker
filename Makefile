report:
	@python tools/reporter.py

# Test target; run a few modules without logging

test:
	make testOkNoOp.run
	make testOkWrite.run
	make testOkReadWrite.run

# Run a specific module in sandbox mode

%.run:
	make $*.clean
	cd modules; make $*.run
	make $*.archive
	make after-run

%.archive:
	cd modules; make $*.archive

%.debug:
	make $*.clean
	cd modules; make $*.debug

# Comprehensive clean target; remove temporary files

%.clean:
	python tools/cleaner.py $*.config

# Internal target: things to be done before a run

before-run:
	@make mkWeb -s
	@make ../101logs -s
	@make ../101temps -s
	@make ../101results -s
	@rm -f ../101logs/runner.log

# Internal target: things to be done after a run

after-run:
	@git pull -q # upgrade past every run

# Target for git-related convenience

push:
	git commit -a
	git push

# Internal target: make sure 101web directories exists.

mkWeb:
	@mkdir -p ../101web
	@mkdir -p ../101web/data
	@mkdir -p ../101web/data/dumps
	@mkdir -p ../101web/data/resources
	@mkdir -p ../101web/data/resources/contributions
	@mkdir -p ../101web/data/resources/languages
	@mkdir -p ../101web/data/resources/technologies

# Internal target: make sure 101logs directory exists.

../101logs:
	@mkdir ../101logs

# Internal target: make sure 101temps directory exists.

../101temps:
	@mkdir ../101temps

# Internal target: make sure 101results directory exists.

../101results:
	@mkdir ../101results

# Full reset; essentially ALL derived files are brutally removed.
full-reset:
	@rm -rf ../101web
	@rm -rf ../101logs
	@rm -rf ../101temps
	@rm -rf ../101results
