include ../Makefile.vars

run:
	@php Wiki101JsonToWiki101Rdf.php  ${wiki101FullCoreFilename} ${wiki101SchemaERS}
	cp ${configdir}/${wiki101SchemaERS} ${webdir}/dumps/${wiki101SchemaERS}

clean:

