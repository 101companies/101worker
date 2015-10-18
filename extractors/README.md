
# Extractors

The extractors will be executes by the the extract101 module of the 101worker. It determines which extractor should be
executed for which file by reading the language meta-value. If you want to add a new extractor make sure the folder is called like the language meta-key e.g. Java.
Further create an executable  file with the name "extractor". Besides that you should provide a readme file and a Makefile.
The Makefile shall at least have follow labels:

    - test: Runs a/the test case(s)
    - install: Install all dependencies.




To run the extractors some modules/libraries and runtime environments have to be installed on the  machine.
The follow file should give a short overview about those. They will however be automatic installed by the execution of ./install in the 101worker tree.
If you add a new extractor make sure that the needed packadges will be installed. The OS shall be Ubuntu


**Testing*
To test all the extractors simply run the test script in that location: perl test

**Runtime Environemnts**:

* Python (plus pip)
* Haskell (plus Cabal)
* NodeJS (NPM would be recommand in case it wasn't' part of the NodeJS installation')
* Mono (if you are on Windows you would need the .NET framework)
* Java

Further have the follow modules to be installed:

**Python Modules**:
* sqlparse
* HTMLParser

**Haskell Module**:
* JSON
**Javascript**:
* Esprima





