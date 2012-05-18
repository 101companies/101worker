include ../Makefile.vars

run: ${pulledLibrariesDir}
	php pullLibraries.php ${pulledLibrariesConfig} `cd ${workerTimeLibrariesDir};pwd` `cd ${webTimeLibrariesDir};pwd` `cd ${basedir};pwd`
	
${pulledLibrariesDir}:
	mkdir ${pulledLibrariesDir}

clean:
	rm -f -r ${pulledLibrariesDir}
