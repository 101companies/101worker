include ../Makefile.vars

run: ${web101RepoDir}
	touch ${web101RepoDir}/contributions/sourceDirectoryScanning.started ; \
	rm -f ${web101RepoDir}/contributions/sourceDirectoryScanning.done ; \
	php scanSourceFileSystem.php ${pulled101RepoDir} ${web101RepoDir} contributions ${sourceDirectoryMatchingRules} ${sourceDirectoryScanningMethod} ;\
	touch ${web101RepoDir}/contributions/sourceDirectoryScanning.done ;
		
	
${web101RepoDir}:
	mkdir ${web101RepoDir}

clean:
	rm -f -r ${web101RepoDir}
