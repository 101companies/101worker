build:
	@echo nothing to do

test:	test-positive test-negative test-css

test-positive:
	./validator html5_example.html

test-negative:
	./validator department.html -negative

test-css:
	./validator style.css
