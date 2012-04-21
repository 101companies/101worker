include ../Makefile.vars
repo = ${resultsdir}/101repo
dev = ${resultsdir}/101dev
geshi = ${resultsdir}/geshi
xsdClasses = ${dev}/sandbox/m12/implementations/xsdClasses/docs
oxMapping = capabilities/Object_XML_mapping/MegaL/docs

run: ${repo} ${geshi} ${xsdClasses} ${resultsdir}/101repo/${oxMapping}/report.pdf
	@make prepare
	@make geshify
	@make xsdClasses
	@make oxMapping

prepare:
	@rm -rf ${webdir}/MegaModels
	@mkdir ${webdir}/MegaModels
	@mkdir ${webdir}/MegaModels/capabilities
	@mkdir ${webdir}/MegaModels/technologies
	@mkdir ${webdir}/MegaModels/implementations

geshify:
	@python program.py ${repo}

%.geshi:
	@echo $*
	@mkdir -p ${webdir}/MegaModels/${dir ${subst ${repo},,$*}}
	@php ${geshi}/run.php $* ${webdir}/MegaModels${subst ${repo},,$*}.html megal

xsdClasses:
	@echo Publishing browsable megamodel for 101implementation:xsdClasses
	@cp -r ${xsdClasses} ${webdir}/MegaModels/implementations/xsdClasses

oxMapping:
	@echo Publishing LaTeX-ed megamodel for capabilities/Object_XML_mapping
	@mkdir -p ${webdir}/MegaModels/${oxMapping}
	@cp ${resultsdir}/101repo/${oxMapping}/report.pdf ${webdir}/MegaModels/${oxMapping}

${resultsdir}/101repo/${oxMapping}/report.pdf:
	@cd ${resultsdir}/101repo/${oxMapping}; make

clean:
	@cd ${oxMapping}; make clean
