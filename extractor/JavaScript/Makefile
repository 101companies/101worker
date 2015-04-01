# Parser is not supporting depracated single-tags line <br>
# The problem is, it is searching for a closing tag


# Node: These were created as White-Box tests with the aim of executing every if statement at least once.
# However the Javascipt file seems to be somewhat incomplete because not all cases produce an output
.PHONY: test
test:
	mkdir -p test/output
	./extractor < test/ForLoopTest.js > test/output/ForLoop.json
	./extractor < test/FunctionVariableDeclarationTest.js > test/output/FunctionVariableDeclaration.json
	./extractor < test/VariableDeclarationTest.js > test/output/VariableDeclaration.json
	./extractor < test/WhileLoopTest.js > test/output/WhileLoop.json
	./extractor < test/DeepRecursionTest.js > test/output/DeepRecursionTest.json


	diff --ignore-all-space test/output/ForLoop.json test/baseline/ForLoopTestOutput.json
	diff --ignore-all-space test/output/FunctionVariableDeclaration.json test/baseline/FunctionVariableDeclarationTestOutput.json
	diff --ignore-all-space test/output/VariableDeclaration.json test/baseline/VariableDeclarationTestOutput.json
	diff --ignore-all-space test/output/WhileLoop.json test/baseline/WhileLoopTestOutput.json
	diff --ignore-all-space test/output/DeepRecursionTest.json test/baseline/DeepRecursionTestOutput.json


	make reset-test
	
reset-test:
	@rm -f test/output/*.json

clean: 
	make reset-test
install:
	npm install esprima


