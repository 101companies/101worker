include ../Makefile.vars

run: ${pulled101RepoDir} ${dumpsDir} ${contrDir} ${matchesDump}
	@./program.py
	@test -e ${extractorDump}

# Remove local temporary files, if any
clean:
	@#no-op

# Remove files created by this module
reset:
	@rm -f ${extractorDump}
	@find ${contrDir} -name "*.extractor.json" -exec rm -f {} \;

install:
	apt-get install haskell-platform openjdk-7-jdk
	pip install sqlparse
