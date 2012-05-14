include ../Makefile.vars

run:
	@make prepare
	@make deploy


prepare:
	@rm -rf ${webdir}/MegaLExplorer
	@mkdir ${webdir}/MegaLExplorer
	@mkdir ${webdir}/MegaLExplorer/css
	@mkdir ${webdir}/MegaLExplorer/js


deploy:
	@cp ${pulled101DevDir}/sandbox/m12/show.html ${webdir}/MegaLExplorer/