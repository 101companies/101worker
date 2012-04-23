include ../Makefile.vars

run: ${resultsdir}/php-github-api
	cd ${resultsdir}/php-github-api; \
	git pull -q

${resultsdir}/php-github-api:
	@cd ${resultsdir}; \
	git clone https://github.com/ornicar/php-github-api	