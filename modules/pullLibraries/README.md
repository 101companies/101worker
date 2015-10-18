populate directory(ies) "libraries" according to a library specification files. 

# Summary

This module creates or update the "libraries" directories in the worker-time
and web-time spaces. This makes it possible to have libraries in both spaces,
or only in one depending at which time the library is used. 
This module download/create/pull the libraries according to their type and
their specifications given in a .libraries.json file.


# Library types

The term libraries refer to different kind of artefacts that can be used and
shared by 101 modules and/or technologies. They are copied from an external
source to the "libraries" directory(ies).

Currently the following sources are supported:
* "github". Given the repository name, the module make a pull of it.
* "directory". Given a directory path, a copy of the directory if performed.
* "urls". Given a set of url, the files are downloaded.


# Library specifications

Libraries specifications are provided as json map (see the illustration below)
* the key represent the library name. It will be also the directory name in
  which the libraries will be available. For instance arc2 library will go
  into .../libraries/arc2  directory
* "summary" : a summary explaining the purpose of the library
* "language" : the language in which the library is written
* "workertime" : if set to "yes" the library will be copied in the worker space
* "webtime" : if set to "yes" the library will be copied in the web space
* "updates" : if set to "onlyOnce" the library will created but not updated
              if set to "automatic" it will be pulled, copied, download for each 
              mmodule execution.
The following attributes are exclusive and indicates the library source
* "github" : the name of the repository on git hub)
* "directory" : the name of directory to copy 
* "urls" : a map of urls -> filename


# Illustration

The example below show the definition of three libraries corresponding to
three different kind of sources (github, directory, urls).

	{
	  "php-github-api" : {
	      "summary":"github API in php", 
	      "github":"ornicar/php-github-api",
	      "language":"php",      
	      "workertime":"yes",
	      "webtime":"yes",
	      "updates":"automatic"
	    },
	  "geshi" : {
	      "summary":"source code highlighting based on simple lexical language definitions",
	      "dir" : "101results/101repo/technologies/geshi/src",
	      "comment" : "copied from the technologies directory because there is no way to easily get the last version", 
	      "language":"php",
	      "workertime":"yes",
	      "updates":"automatic"
	    }, 
	  "sigmajs" : {
	      "summary":"JavaScript library to draw graphs",
	      "urls":{
	        "http://sigmajs.org/js/sigma.min.js" : "sigma.min.js" 
	      },
	      "language":"javascript",
	      "webtime":"yes",
	      "updates":"onlyOnce"
	    }
	}
