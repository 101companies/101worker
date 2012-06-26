include ../Makefile.vars
results = 	${resultsdir}/101meta/rules.json \
		${resultsdir}/101meta/matches.json \
		${resultsdir}/101meta/summary.json \
		${resultsdir}/101meta/validation.json \
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
	cd ../aggregate101meta; make
	cd ../validate101meta; make
	make
