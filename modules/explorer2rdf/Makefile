include ../Makefile.vars
output = ${dumpsDir}/explorer.rdf

run:
	@./gather.py
	@./combine.py
	@cp complete.rdf ${output}

validate:
	java -jar CIMValidate-20010909a.jar ${output} ../../services_temp/discovery/schemas/repo.rdfs

clean:
	rm -f ${output}
	rm -f *.nt
	rm -f *.rdf