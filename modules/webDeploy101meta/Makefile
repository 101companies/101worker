include ../Makefile.vars
results = 	${resultsdir}/101meta/rules.json \
		${resultsdir}/101meta/matches.json \
		${resultsdir}/101meta/summary.json
web = ${webdir}/101meta

run: ${results} ${web}
	@cp ${results} ${web}

${web}:
	@mkdir ${web}

# Remove local temporary files if any
clean:  
	@#no-op

# Complete local run by presupposed runs
run-all:
	cd ../aggregate101meta; make run-all
	make run
