include ../Makefile.vars

run: ${web101RepoDir}
	php scanSourceFileSystem.php ${pulled101RepoDir} ${web101RepoDir} contributions ${sourceDirectoryMatchingRules} ${sourceDirectoryScanningMethod}
	
${web101RepoDir}:
	mkdir ${web101RepoDir}

clean:
	rm -f -r ${web101RepoDir}
