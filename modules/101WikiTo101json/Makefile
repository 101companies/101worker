include ../Makefile.vars
basic = ${tempsdir}/dumps/Wiki101Full.json
linkified = ${webdir}/dumps/Wiki101FullLinkified.json

run:
	@php jsongenerator.php ${basic}
	@python text2list.py ${basic} ${linkified}

clean:

