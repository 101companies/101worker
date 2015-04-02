To run the extractors some modules/libraries and runtime environments have to be installed on the  machine.
The follow file should give a short overview about those

Runtime Environemnts:
	- Python
	- Haskell
	- NodeJS (NPM would be recommand in case it wasn't' part of the NodeJS installation')
	- Mono (if you are on Windows you would need the .NET framework)
	- Java

Further have the follow modules to be installed:

Python Modules:
	- sqlparse
	- HTMLParser

Haskell Module:
	- JSON-Combinator
Javascript:
    - Esprima



To run the test you can simply execute the "make run-test" line in the specific subfolder. However not every extractor provides
a test case.

