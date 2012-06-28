include ../Makefile.defs

run: ${repoDir} ${geshiDir} ${matchesDump} ${contrDir}
	@./program.py ${geshi}/run.php
	@test -e ${geshiDump}

# Remove local temporary files, if any
clean:	
	@#no-op

# Remove files created by this module
reset:
	@find ${contrDir} -name "*.geshi.html" -exec rm -f {} \;

# Complete local run by presupposed runs
run-all:
	cd ../match101meta; make run-all
	make run
