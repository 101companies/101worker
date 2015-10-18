include ../Makefile.vars
repo = ${resultsdir}/101repo
antlr = ${repo}/technologies/ANTLR/antlr-3.2.jar
parser = ${repo}/languages/MegaL/parser

run: ${repo} ${parser}
	@cd ${parser}; make -s
	@python program.py ${repo}

%.parse:
	java -cp ${parser}:${antlr} megal.parser.Main $*

clean:
	@cd ${parser}; make clean
