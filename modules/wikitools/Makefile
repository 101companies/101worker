include ../Makefile.vars

run:
	make up	
	mkdir -p tex/sources
	python main.py
up:
	git pull
	cd ../../libraries; git pull
publish:
	tar -cvvf tex.tar tex
	rm -r ${webdir}/texgen
	mkdir -p ${webdir}/texgen
	cp tex.tar ${webdir}/texgen
clean:
	rm -r tex/sources/*.src
	rm tex.tar
