include ../Makefile.vars

run: ${pulled101RepoDir} ${dumpsDir} ${contrDir} ${matchesDump}
	@./program.py
	@test -e ${metricsDump}

# Remove local temporary files, if any
clean:	
	@#no-op

# Remove files created by this module
reset:
	@rm -f ${metricsDump}
	@find ${contrDir} -name "*.metrics.json" -exec rm -f {} \;
