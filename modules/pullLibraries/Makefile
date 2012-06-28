include ../Makefile.vars

run: ${workerTimeLibrariesDir} ${webTimeLibrariesDir}
	php pullLibraries.php ${pulledLibrariesConfig} ${workerTimeLibrariesDir} ${webTimeLibrariesDir} ${basedir}
	
${workerTimeLibrariesDir}:
	@ mkdir ${workerTimeLibrariesDir}
	
${webTimeLibrariesDir}:
	@ mkdir ${webTimeLibrariesDir}

clean:
	rm -f -r ${workerTimeLibrariesDir} ${webTimeLibrariesDir}
