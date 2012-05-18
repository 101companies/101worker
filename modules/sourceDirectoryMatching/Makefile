include ../Makefile.vars

run: ${web101RepoDir}
	php matchSourceDirectory.php ${sourceDirectoryMatchingRules} ${pulled101RepoDir} ${web101RepoDir} contributions
	
${web101RepoDir}:
	@ mkdir -f ${web101RepoDir}
	@ mkdir -f ${web101RepoDir}/contributions
	
clean:
	rm -f -r ${web101RepoDir}
