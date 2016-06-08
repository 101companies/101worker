include ../Makefile.vars

run: ${pulled101RepoDir} ${gatheredGeshiDir} ${matchesDump} ${contrDir}
	@./program.py ${gatheredGeshiDir}/run.php
	@test -e ${geshiDump}

# Remove local temporary files, if any
clean:	
	@#no-op

# Remove files created by this module
reset:
	@find ${contrDir} -name "*.geshi.html" -exec rm -f {} \;

