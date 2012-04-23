include ../Makefile.vars

run: ${resultsdir}/megalib
	cd ${resultsdir}/megalib; \
	git pull -q

${resultsdir}/megalib:
	@cd ${resultsdir}; \
	git clone https://github.com/megaplanet/megalib	
