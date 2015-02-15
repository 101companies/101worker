# Creates a report with the last execution results and sends an email
report:
	@python tools/reporter.py

# Run something given in configs/env/$*.yml
%.run:
	cd modules; make $*.run
	make $*.archive
	@git pull -q # upgrade past every run

# Like %.run but without logging, with stdout
%.debug:
	cd modules; make $*.debug

# Arcives the log files from the last execution
%.archive:
	mkdir -p ../101web/logs
	cd modules; make $*.archive

# Remove ALL derived files
full-reset:
	@rm -rf ../101web ../101logs ../101temps ../101results ../101diffs

download:
	cd modules/zip; make download-and-extract
