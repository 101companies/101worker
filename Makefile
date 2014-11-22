# Creates a report with the last execution results and sends an email
report:
	@python tools/reporter.py

# Run modules of a .config file
%.run: init
	make $*.clean
	cd modules; make $*.run
	tools/filedepend ../101results/depend configs/$*.json \
                   > ../101results/depend/graph.yml
	make $*.archive
	@git pull -q # upgrade past every run

# Like %.run but without logging, with stdout
%.debug:
	make $*.clean
	cd modules; make $*.debug

# Arcives the log files from the last execution
%.archive:
	mkdir -p ../101web/logs
	cd modules; make $*.archive

# What is this?
%.clean:
	python tools/cleaner.py $*.json

# Remove ALL derived files
full-reset:
	@rm -rf ../101web
	@rm -rf ../101logs
	@rm -rf ../101temps
	@rm -rf ../101results

# Initialize output directories
init:
	@mkdir -p ../101logs
	@mkdir -p ../101temps
	@mkdir -p ../101results
	@mkdir -p ../101web
	@mkdir -p ../101web/data
	@mkdir -p ../101web/data/dumps
	@mkdir -p ../101web/data/resources
	@mkdir -p ../101web/data/views
	@mkdir -p ../101web/data/onto
	@mkdir -p ../101web/data/resources/contributions
	@mkdir -p ../101web/data/resources/languages
	@mkdir -p ../101web/data/resources/technologies
	@mkdir -p ../101web/data/resources/themes
	@mkdir -p ../101web/logs

# Git-related convenience
push:
	git commit -a
	git push

download:
	make init
	cd modules/zip; make download-and-extract
