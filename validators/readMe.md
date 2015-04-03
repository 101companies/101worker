The validators will be executes by the the validate101 module of the 101worker. It determines which validators should be
executed for which file by reading the validator meta-value. That key has as value the foldername in that directory. Follow
rule would refer to the JValidator:

{
"suffix"    : ".java"
"metadata   :" [  {geshi: "java"},
                  {language: "Java"},
                  {validator: "JValidator"},
               ]
}

Further create an executable  file with the name "validate". Besides that you should provide a readme file and a Makefile.
The Makefile shall at least have follow labels:
    - test: Runs a/the test case(s)
    - install: Install all dependencies.




To run the validator some modules/libraries and runtime environments have to be installed on the  machine.
The follow file should give a short overview about those. They will however be automatic installed by the execution ./install in the 101worker tree.
If you add a new extractor make sure that the needed packadges will be installed. The OS shall be Ubuntu


Runtime Environemnts:
    - Python
	- Java (especially make sure javac is included)






