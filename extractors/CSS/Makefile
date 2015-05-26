# Comments are not supported.
.PHONY: test
test: 
	mkdir -p test/output
	./extractor < test/Declaration.css > test/output/Declaration.json
	./extractor < test/Rule.css > test/output/Rule.json

	diff --ignore-all-space test/baseline/Declaration.json test/output/Declaration.json
	diff --ignore-all-space test/baseline/Rule.json test/output/Rule.json

	make reset-test
	
reset-test:
	@rm -f test/output/*.json

clean: 
	make reset-test

install:
	pip install tinycss
