include ../Makefile.vars

run: ${pulledLibrariesDir}
	php pullLibraries.php ${pulledLibrariesConfig} `cd ${pulledLibrariesDir};pwd` `cd ${basedir};pwd`
	
${pulledLibrariesDir}:
	mkdir ${pulledLibrariesDir}

clean:
	rm -r ${pulledLibrariesDir}
