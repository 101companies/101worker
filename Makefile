# Run something given in configs/env/$*.yml
# There's a chicken-and-egg problem with 101logs: the runner's output is
# supposed to be piped into 101logs/runner.log, but the runner is what
# creates the folders in the first place. To solve it, the 101logs folder
# is created here if it doesn't exist.
%.run:
	mkdir -p ../101logs
	rm -f ../101logs/*
	cd modules; make $*.run
	make $*.archive
	@git pull -q # upgrade past every run


# Like %.run but without logging, with stdout
%.debug:
	cd modules; make $*.debug


# Debug, gather changes and build dependency graph in GraphViz format.
# The dot command needs to be available generate a PDF.
# Everything dependency-related goes into ../101diffs
%.depend:
	rm -f ../101diffs/*.changes
	runner101depend=1 make $*.debug
	tools/depend ../101diffs/*.changes > ../101diffs/$*.dot
	dot -Tpdf <../101diffs/$*.dot >../101diffs/$*.pdf


# Archives the log files from the last execution
%.archive:
	tools/archiver


# Remove ALL derived files
full-reset:
	rm -rf ../101web ../101logs ../101temps ../101results ../101diffs


download:
	cd modules/zip; make download-and-extract
