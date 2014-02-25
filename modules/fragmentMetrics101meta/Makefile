include ../Makefile.vars

run:
	@./program.py

# Remove files created by this module
reset:
	@rm -f ${fragmentMetricsDump}
	@find ${contrDir} -name "*.fragments.metrics.json" -exec rm -f {} \;
	@find ${contrDir} -name "*.fragments.tokens.json" -exec rm -f {} \;

