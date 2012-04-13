runner = tools/runner.sh
testSucceed = testSucceedNoOp testSucceedWrite testSucceedReadWrite
modules = ${testSucceed}

run:
	@echo Performing all registered modules
	@make prepare -s
	@make $(patsubst %, %.run, ${modules}) -s

%.run:
	@${runner} $*

prepare:
	@make ../101temps -s
	@make ../101results -s

push:
	git commit -a
	git push

../101temps:
	@mkdir ../101temps

../101results:
	@mkdir ../101results
