build:
	@echo nothing to do

test: test-positive test-negative

test-positive:
	./validator ./test/goodexample.html -verbose

test-negative:
	./validator ./test/badexample.html -verbose -negative
