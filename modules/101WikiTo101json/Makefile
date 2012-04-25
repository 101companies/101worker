include ../Makefile.vars
basic = ${tempsdir}/Wiki101FullTemp.json
linkified = ${webdir}/Wiki101Full.json

run:
	@php jsongenerator.php ${basic}
	@python text2list.py ${basic} ${linkified}

clean:
	rm -f ${basic}

