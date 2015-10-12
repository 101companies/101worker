# Comments not supported
.PHONY: test
test:
	mkdir -p test/output
	./extractor < test/AlterStatement.sql > test/output/AlterStatement.json
	./extractor < test/Column.sql > test/output/Column.json
	./extractor < test/CreateStatement.sql > test/output/CreateStatement.json
	./extractor < test/IndexedAlterStatement.sql > test/output/IndexedAlterStatement.json
	./extractor < test/BugIndexingMixCreateStatements.sql > test/output/BugIndexingMixCreateStatements.json
	
		
	diff --ignore-all-space test/baseline/AlterStatement.json test/output/AlterStatement.json
	diff --ignore-all-space test/baseline/Column.json test/output/Column.json
	diff --ignore-all-space test/baseline/CreateStatement.json test/output/CreateStatement.json
	diff --ignore-all-space test/baseline/IndexedAlterStatement.json test/output/IndexedAlterStatement.json
	diff --ignore-all-space test/baseline/BugIndexingMixCreateStatements.json test/output/BugIndexingMixCreateStatements.json

	make reset-test
	
reset-test:
	@rm -f test/output/*.json

clean: 
	make reset-test

install:
	pip install sqlparse