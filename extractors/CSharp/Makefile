build:
	make CSharp/CSharpFactExtractor.exe

CSharp/CSharpFactExtractor.exe: extractors/*.cs Makefile
	mkdir -p bin
	dmcs \
			-target:exe -out:bin/extractor.exe \
			-lib:./lib -reference:Mono.Cecil.dll -reference:ICSharpCode.NRefactory.dll -reference:ICSharpCode.NRefactory.CSharp.dll \
			-reference:ICSharpCode.NRefactory.Tests.dll -reference:ICSharpCode.NRefactory.Xml.dll \
			extractors/*.cs
	cp lib/*.dll bin
	cp lib/*.so bin

.PHONY: test
test:
	make build
	mkdir -p test/output
	@./extractor < Company.cs > Company.cs.facts.json
	@diff --ignore-all-space simple.baseline Company.cs.facts.json
	@echo Tests passed

clean:
	rm -rf bin/*.exe
	rm -rf bin/*.dll
	rm -rf bin/*.so
	rm -f Company.cs.facts.json
	
.PHONY: install
install:
	apt-get install mono-complete
	apt-get install mono-dmcs
