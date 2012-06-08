include ../Makefile.vars

run:
	@make prepare
	@make deploy


prepare:
	@rm -rf ${webdir}/MegaLExplorer
	@mkdir ${webdir}/MegaLExplorer
	@mkdir ${webdir}/MegaLExplorer/css
	@mkdir ${webdir}/MegaLExplorer/js
	@mkdir ${webdir}/MegaLExplorer/js/_lib
	@mkdir ${webdir}/MegaLExplorer/js/themes/
	@mkdir ${webdir}/MegaLExplorer/js/themes/default/
	@mkdir ${webdir}/MegaLExplorer/imgs


deploy:
	@cp ${pulled101DevDir}/sandbox/m12/*.* ${webdir}/MegaLExplorer/
	@cp ${pulled101DevDir}/sandbox/m12/js/*.js ${webdir}/MegaLExplorer/js/
	@cp ${pulled101DevDir}/sandbox/m12/js/_lib/*.js ${webdir}/MegaLExplorer/js/_lib/
	@cp ${pulled101DevDir}/sandbox/m12/js/themes/default/style.css ${webdir}/MegaLExplorer/js/themes/default/style.css
	@cp ${pulled101DevDir}/sandbox/m12/js/themes/default/d.png ${webdir}/MegaLExplorer/js/themes/default/d.png
	@cp ${pulled101DevDir}/sandbox/m12/css/*.css ${webdir}/MegaLExplorer/css/
	@cp ${pulled101DevDir}/sandbox/m12/imgs/*.* ${webdir}/MegaLExplorer/imgs/