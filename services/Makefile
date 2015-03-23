install:
	echo $(DJANGO_ENV)
	DJANGO_ENV=$(DJANGO_ENV) ./deploy.py

pp = PYTHONPATH="$$PYTHONPATH:$$(dirname $$(pwd))"

test:
	${pp} prove --ext=.t.py -e 'python -W ignore'

cover:
	rm -rf .coverage htmlcov
	for f in t/*.t.py; \
	do \
	${pp} coverage run -a --branch --source=. '--omit=t/*.t.py' "$$f"; \
	done;
	coverage html
	@echo See htmlcov/index.html for coverage output.

clean:
	rm -rf .coverage htmlcov
