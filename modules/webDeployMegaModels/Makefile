include ../Makefile.vars
repo = ${resultsdir}/101repo
geshi = ${resultsdir}/geshi
xsdClasses = ../../../101dev/sandbox/m12/implementations/xsdClasses/docs

run: ${repo} ${geshi}
	@rm -rf ${webdir}/MegaModels
	@mkdir ${webdir}/MegaModels
	@mkdir ${webdir}/MegaModels/capabilities
	@mkdir ${webdir}/MegaModels/technologies
	@mkdir ${webdir}/MegaModels/implementations
	@python program.py ${repo}
	@echo Publishing browsable megamodel for 101implementation:xsdClasses
	@cp -r ${xsdClasses} ${webdir}/MegaModels/implementations/xsdClasses

%.geshi:
	@echo $*
	@mkdir -p ${webdir}/MegaModels/${dir ${subst ${repo},,$*}}
	@php ${geshi}/run.php $* ${webdir}/MegaModels${subst ${repo},,$*}.html megal

clean:
	@# no-op
