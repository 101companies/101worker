
# Validators

The validators will be executes by the the validate101meta module of the 101worker. The use of that scripts is to validate if a specific file is really  of the language it was assigned to by the rules (http://data.101companies.org/dumps/rules.json). It determines which validator
should be executed for which file by reading the language meta-value. Hence a file that was classified as file that is written in the language Java will be validated by the Java validator.
Every language that posses a validator has a subfolder in the validator direction that is named like the language meta-key.

Follow rule would therefore refer to the validator/Java/validator executable file:

```
{
"suffix"    : ".java"
"metadata   :" [  {geshi: "java"},
                  {language: "Java"},
               ]
}
```
If you want to code a new validator make sure to do follow steps:

Create an executable  file with the name "validate". Besides that you should provide a readme file and a Makefile.
The Makefile shall at least have follow labels:
* test: Runs a/the test case(s)
* install: Install all dependencies.

To run the validator some modules/libraries and runtime environments have to be installed on the  machine.
The follow file should give a short overview about those. They will, however, be automatic installed by the execution of ./install in the 101worker tree.
If you add a new validator make sure that the needed packadges will be installed. The OS shall be Ubuntu

**Testing**:

To run all the validator  test cases enter the following command in your terminal while being in that folder:
* perl test

**Runtime Environemnts**:
* Python
* Java (especially make sure javac is included)
* C# (mono)






