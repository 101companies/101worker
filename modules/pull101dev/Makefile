include ../Makefile.vars

run: ${resultsdir}/101dev
	cd ${resultsdir}/101dev; \
	git pull -q

${resultsdir}/101dev:
	@cd ${resultsdir}; \
	git clone https://github.com/101companies/101dev
