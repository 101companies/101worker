# Comments are not supported.
.PHONY: test
test:
	mkdir -p test/output
	./extractor < test/IndexedObject.json > test/output/IndexedObject.json
	./extractor < test/List.json > test/output/List.json
	./extractor < test/Object.json > test/output/Object.json

	diff --ignore-all-space test/baseline/IndexedObject.json test/output/IndexedObject.json
	diff --ignore-all-space test/baseline/List.json test/output/List.json
	diff --ignore-all-space test/baseline/Object.json test/output/Object.json

	make reset-test
	
reset-test:
	@rm -f test/output/*.json

clean: 
	make reset-test
