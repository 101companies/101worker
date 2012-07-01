include ../Makefile.vars

run:
	@php wiki101JsonToWiki101RDF.php ${wiki101FullCoreFilename} ${configsdir}/${wiki101SchemaERS}

clean:
	@ mv ${wiki101FullCoreFilename}.json /tmp/backup-$$
	rm ${wiki101FullCoreFilename}.*
	@ mv /tmp/backup-$$ ${wiki101FullCoreFilename}.json

