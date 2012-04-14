runner = python tools/runner.py
cleaner = python tools/cleaner.py
testSucceed = testSucceedNoOp testSucceedWrite testSucceedReadWrite
modules = ${testSucceed}

run:
	@echo Performing all modules.
	@make prepare -s
	@make $(patsubst %, %.run, ${modules}) -s

clean:
	@rm -f logs/runner.log
	@make $(patsubst %, %.clean, ${modules}) -s

%.run:
	@${runner} $*

%.clean:
	@${cleaner} $*

prepare:
	@make ../101temps -s
	@make ../101results -s
	@rm -f logs/runner.log

push:
	git commit -a
	git push

../101temps:
	@mkdir ../101temps

../101results:
	@mkdir ../101results
