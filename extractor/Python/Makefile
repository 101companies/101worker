# Parser is not supporting depracated single-tags line <br>
# The problem is, it is searching for a closing tag

# Node: These were created as White-Box tests with the aim of executing every if statement at least once.
# However apparently the code doesn't list the variables in the except part


.PHONY: test
test:
	./extractor < test/simpleClassTest.py > test/output/SimpleClass.json
	#Apparently the code doesn't list the variables in the except part
	./extractor < test/simpleExceptionTest.py > test/output/SimpleException.json
	./extractor < test/simpleForTest.py  > test/output/SimpleFor.json
	./extractor < test/simpleFunc.py > test/output/SimpleFunc.json
	./extractor < test/simpleImportTest.py > test/output/SimpleImport.json
	./extractor < test/simpleWhileTest.py  > test/output/SimpleWhile.json

	diff --ignore-all-space test/output/SimpleClass.json test/baseline/SimpleClass.json

	#Apparently the code doesn't list the variables in the except part
	diff --ignore-all-space test/output/SimpleException.json test/baseline/SimpleException.json
	diff --ignore-all-space test/output/SimpleFor.json test/baseline/SimpleFor.json
	diff --ignore-all-space test/output/SimpleFunc.json test/baseline/SimpleFunc.json
	diff --ignore-all-space test/output/SimpleImport.json test/baseline/SimpleImport.json
	diff --ignore-all-space test/output/SimpleWhile.json test/baseline/SimpleWhile.json


	make reset-test

reset-test:
	@rm -f test/output/*.json

clean:
	make reset-test


