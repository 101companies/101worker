runner = tools/runner.sh
testSucceed = testSucceedNoOp testSucceedWrite testSucceedReadWrite
modules = ${testSucceed}

run:
	@echo Performing all registered modules
	@make prepare
	@make $(patsubst %, %.run, ${modules})

%.run:
	@${runner} $*

prepare:
	@make ../101temps -s
	@make ../101results -s

../101temps:
	@mkdir ../101temps

../101results:
	@mkdir ../101results
