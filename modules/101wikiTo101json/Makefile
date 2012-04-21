include ../Makefile.vars
env = ${webdir}
basic = ${env}/all.json
linkified = ${env}/allLinkified.json

run:
	@php jsongenerator.php ${basic}
	@python text2list.py ${basic} ${linkified}

