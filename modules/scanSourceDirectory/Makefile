include ../Makefile.vars

run: ${web101RepoDir}
	php scanSourceDirectory.php ${pulled101RepoDir} ${web101RepoDir} contributions
	
${web101RepoDir}:
	mkdir ${web101RepoDir}

clean:
	rm -f -r ${web101RepoDir}
