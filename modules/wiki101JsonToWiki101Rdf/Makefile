include ../Makefile.vars

run:
	@php Wiki101JsonToWiki101Rdf.php ${wiki101FullCoreFilename} ${configsdir}/${wiki101SchemaERS}
	cp ${configsdir}/${wiki101SchemaERS} ${webdir}/dumps/${wiki101SchemaERS}

clean:

