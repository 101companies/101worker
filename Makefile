# Run something given in configs/env/$*.yml
%.run:
	# There's a chicken-and-egg problem with 101logs: the runner's output is
	# supposed to be piped into 101logs/runner.log, but the runner is what
	# creates the folders in the first place. To solve it, the 101logs folder
	# is created here if it doesn't exist.
	mkdir -p ../101logs
	rm -f ../101logs/* # Logs are archived, so they're cleared on every run.
	cd modules; make $*.run
	make $*.archive
	@git pull -q # upgrade past every run


# Like %.run but without logging, with stdout
%.debug:
	# The debug runner output isn't piped into 101logs, so in this case we can
	# fall back to the runner creating all directories.
	cd modules; make $*.debug


# Archives the log files from the last execution
%.archive:
	tools/archiver


# Remove ALL derived files
full-reset:
	rm -rf ../101web ../101logs ../101temps ../101results ../101diffs


download:
	cd modules/zip; make download-and-extract
