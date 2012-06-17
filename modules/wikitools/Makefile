include ../Makefile.vars

run:
	make up	
	mkdir -p tex/sources
	python main.py
up:
	git pull
	cd ../../libraries; git pull
publish:
	@no-op
clean:
	rm -r tex/sources/*.src
