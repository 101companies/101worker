# Main target; run all modules

run:
	@echo Performing all modules.
	@make clean
	@make before-run -s
	@cd modules; make run -s
	@make after-run -s

report:
	@python tools/mailer.py

# Test target; run a few modules without logging

test:
	make testOkNoOp.run
	make testOkWrite.run
	make testOkReadWrite.run

# Run a specific module in sandbox mode

%.run: modules/%/Makefile
	cd modules/$*; make

# Reconfiguration for a module lists

%.reconfigure: configs/%.config
	@cd configs; \
	rm -f current.config; \
	cp $*.config current.config; \
	chmod ugo-w current.config

# Comprehensive reset; essentially all derived files are brutally removed.

reset:
	@make clean
	@rm -rf ../101web
	@rm -rf ../101logs
	@rm -rf ../101temps
	@rm -rf ../101results


# Comprehensive clean target; remove temporary files

clean:
	@python tools/cleaner.py
	@cd modules; make clean -s

# Internal target: things to be done before a run

before-run:
	@make configs/current.config -s
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

# Internal target: use production configuration by default.

configs/current.config: configs/production.config
	make production.reconfigure -s

# Internal target: make sure 101web directories exists.

mkWeb:
	@mkdir -p ../101web
	@mkdir -p ../101web/dumps
	@mkdir -p ../101web/contributions

# Internal target: make sure 101logs directory exists.

../101logs:
	@mkdir ../101logs

# Internal target: make sure 101temps directory exists.

../101temps:
	@mkdir ../101temps

# Internal target: make sure 101results directory exists.

../101results:
	@mkdir ../101results
