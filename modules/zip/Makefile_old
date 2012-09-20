include ../Makefile.vars

run: ${webdir}/contributions.tgz

${webdir}/contributions.tgz: ${webdir}/contributions
	cd ${webdir} ; pwd ; tar cf contributions.tar contributions
	gzip -9 ${webdir}/contributions.tar 
	rm -f ${webdir}/contributions.tgz
	mv ${webdir}/contributions.tar.gz ${webdir}/contributions.tgz 
	
restart-from-zip:
	rm -f ${webdir}/contributions.tar
	gunzip -c ${webdir}/contributions.tgz >${webdir}/contributions.tar
	rm -f -r ${webdir}/contributions
	cd ${webdir} ; pwd ; tar -xf contributions.tar 
	rm -f ${webdir}/contributions.tar

restart-from-worker: download restart-from-zip
		
download:
	rm -f ${webdir}/contributions.tgz
	cd ${webdir} ; wget ${workerWebUrl}contributions.tgz
     
clean:
	rm -f ${webdir}/contributions.tgz
	rm -f ${webdir}/dumps.tgz

