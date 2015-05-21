setup:
	@echo Setting up 101worker - installation of dependencies requires sudo
	./install -y
	./test


install:
	cpan CPAN
	apt-get install -y python-pip build-essential python-dev
	pip install simplejson

deploy:
	apt-get install subversion -y
	svn checkout https://svn.uni-koblenz.de/softlang/101backup/
	cat 101backup/keys >> ~/.bashrc
	runuser -l worker  -c 'uwsgi services/services.ini'

# Run something given in configs/env/$*.yml
# There's a chicken-and-egg problem with 101logs: the runner's output is
# supposed to be piped into 101logs/runner.log, but the runner is what
# creates the folders in the first place. To solve it, the 101logs folder
# is created here if it doesn't exist.
%.run:
	@git pull -q # upgrade before every run
	mkdir -p ../101logs
	rm -f ../101logs/*
	-cd modules; make $*.run
	make archive


# Like %.run but without logging, with stdout
%.debug:
	cd modules; DEBUG101=1 make $*.debug


# Debug, gather changes and build dependency graph in Graphviz format.
# The dot command needs to be available generate a PDF and the tred command
# for transitive reduction.
# Everything dependency-related goes into ../101diffs
%.depend: graphpm dot.graphviz tred.graphviz
	rm -f ../101diffs/*.changes
	runner101depend=1 make $*.debug
	tools/depend ../101diffs/*.changes      >../101diffs/$*.dot
	dot -Tpdf   <../101diffs/$*.dot         >../101diffs/$*.pdf
	tred        <../101diffs/$*.dot         >../101diffs/$*.reduced.dot
	dot -Tpdf   <../101diffs/$*.reduced.dot >../101diffs/$*.reduced.pdf


# Archives the log files from the last execution
archive:
	tools/archiver

# Saves a report to 101logs/(latest log)/report.html
# and sends it per e-mail to 101gatekeepers.
report:
	tools/reporter


# Remove ALL derived files
full-reset:
	rm -rf ../101web ../101logs ../101temps ../101results ../101diffs


download:
	cd modules/zip; make download-and-extract


graphpm:
	@perl -MGraph -e 1; \
	if [ $$? -ne 0 ]; \
	then \
	    echo 'ERROR: Graph.pm not found. Maybe try:' 1>&2; \
	    echo '    sudo cpan Graph'                   1>&2; \
	    exit 1; \
	fi


%.graphviz:
	@type $*; \
	if [ $$? -ne 0 ]; \
	then \
	    echo 'ERROR: Graphviz not found. Maybe try:' 1>&2; \
	    echo '    sudo apt-get install graphviz'     1>&2; \
	    exit 1; \
	fi


.PHONY: full-reset download graphpm graphviz install
