include ../Makefile.vars

run: ${web101RepoDir} 
	php locateFragments.php ${pulled101RepoDir} ${web101RepoDir} contributions ${sourceDirectoryMatchingRules} /tmp ${pulled101RepoDir}/technologies
	
${web101RepoDir}:
	mkdir ${web101RepoDir}

