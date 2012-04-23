include ../Makefile.vars

run: ${resultsdir}/arc2
	cd ${resultsdir}/arc2; \
	git pull -q

${resultsdir}/arc2:
	@cd ${resultsdir}; \
	git clone https://github.com/semsol/arc2	