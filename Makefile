runner = tools/runner.sh

run:
	@echo Performing all registered modules
	make runTestSucceed

runTestSucceed:
	${runner} testSucceedNoOp