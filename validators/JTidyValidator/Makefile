build:
	@echo nothing to do

test: test-positive test-negative

test-positive:
	./validator index.html -verbose

test-negative:
	./validator department.html -verbose -negative
