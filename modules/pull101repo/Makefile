include ../Makefile.vars

run: ${resultsdir}/101repo
	cd ${resultsdir}/101repo; \
	git pull -q

${resultsdir}/101repo:
	@cd ${resultsdir}; \
	git clone https://github.com/101companies/101repo	

clean:
	@rm -f ${temp} ${resultsdir}/101repo
