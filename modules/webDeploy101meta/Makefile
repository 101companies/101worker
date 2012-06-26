include ../Makefile.vars
results = 	${resultsdir}/101meta/rules.json \
		${resultsdir}/101meta/matches.json \
		${resultsdir}/101meta/summary.json \
		${resultsdir}/101meta/validation.json \
		${resultsdir}/101meta/facts \
		${resultsdir}/101meta/geshi
web = ${webdir}/101meta

run: ${results} ${web}
	@cp -r ${results} ${web}

${web}:
	@mkdir ${web}

# Remove local temporary files if any
clean:  
	@#no-op

# Complete local run by presupposed runs
run-all:
	cd ../match101meta; make run-all
	cd ../validate101meta; make
	cd ../extract101meta; make
	cd ../geshi101meta; make
	cd ../aggregate101meta; make
	make
