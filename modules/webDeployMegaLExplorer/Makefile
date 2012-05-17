include ../Makefile.vars

run:
	@make prepare
	@make deploy


prepare:
	@rm -rf ${webdir}/MegaLExplorer
	@mkdir ${webdir}/MegaLExplorer
	@mkdir ${webdir}/MegaLExplorer/css
	@mkdir ${webdir}/MegaLExplorer/js
	@mkdir ${webdir}/MegaLExplorer/imgs


deploy:
	@cp ${pulled101DevDir}/sandbox/m12/show.html ${webdir}/MegaLExplorer/
	@cp ${pulled101DevDir}/sandbox/m12/js/*.js ${webdir}/MegaLExplorer/js/
	@cp ${pulled101DevDir}/sandbox/m12/css/*.css ${webdir}/MegaLExplorer/css/
	@cp ${pulled101DevDir}/sandbox/m12/imgs/*.* ${webdir}/MegaLExplorer/imgs/