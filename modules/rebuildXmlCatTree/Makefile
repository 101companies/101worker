include ../Makefile.vars

run:
	@php rebuild.php ${webdir}/catTreeTemp.xml
	mv ${webdir}/catTreeTemp.xml ${webdir}/catTree.xml
	scp ${webdir}/catTree.xml black42.uni-koblenz.de:101web/

clean:
	