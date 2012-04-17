include ../Makefile.vars
repo = ${resultsdir}/101repo
geshi = ${resultsdir}/geshi

run: ${repo} ${geshi}
	@python program.py ${repo}

%.geshi:
	@echo $*
	@mkdir -p ${webdir}${dir ${subst ${repo},,$*}}
	@php ${geshi}/run.php $* ${webdir}${subst ${repo},,$*}.html megal

clean:
	@# no-op
