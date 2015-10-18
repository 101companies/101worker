include ../Makefile.vars

run:
	@make prepare
	@make linkdata
	@make deploy


prepare:
	@rm -rf ${webdir}/101explorer
	@mkdir ${webdir}/101explorer
	@mkdir ${webdir}/101explorer/css
	@mkdir ${webdir}/101explorer/js
	@mkdir ${webdir}/101explorer/js/_lib
	@mkdir ${webdir}/101explorer/js/themes/
	@mkdir ${webdir}/101explorer/js/themes/default/
	@mkdir ${webdir}/101explorer/imgs
	@mkdir ${webdir}/101explorer/images

linkdata: 

	ln -s ~/101web/data/ ~/101web/101explorer/data


deploy:
	@cp ${pulled101DevDir}/sandbox/m12/*.* ${webdir}/101explorer/
	@cp ${pulled101DevDir}/sandbox/m12/js/*.js ${webdir}/101explorer/js/
	@cp ${pulled101DevDir}/sandbox/m12/js/_lib/*.js ${webdir}/101explorer/js/_lib/
	@cp ${pulled101DevDir}/sandbox/m12/js/themes/default/style.css ${webdir}/101explorer/js/themes/default/style.css
	@cp ${pulled101DevDir}/sandbox/m12/js/themes/default/d.png ${webdir}/101explorer/js/themes/default/d.png
	@cp ${pulled101DevDir}/sandbox/m12/css/*.css ${webdir}/101explorer/css/
	@cp ${pulled101DevDir}/sandbox/m12/imgs/*.* ${webdir}/101explorer/imgs/
	@cp ${pulled101DevDir}/sandbox/m12/images/*.* ${webdir}/101explorer/images/