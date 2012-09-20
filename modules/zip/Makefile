include ../Makefile.vars

run:
	make ${webdir}/data/zips

${webdir}/data/zips:	${dumpsDir} ${webdir}/data/resources ${pulled101RepoDir}
	./zipModule.py
	test -e ${webdir}/data/zips

clean:
	@#no-op

reset:
	rm -rf ${webdir}/data/zips
	

