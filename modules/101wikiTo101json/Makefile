include ../Makefile.vars
env = ~/Projects/101/101web
basic = ${env}/all.json
linkified = ${env}/allLinkified.json

run:
	@php jsongenerator.php ${basic}
	@python text2list.py ${basic} ${linkified}

