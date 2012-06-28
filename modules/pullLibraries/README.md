Summary
-------
This module creates or update the "libraries" directories in the worker-time and web-time spaces.
It download/create/pull the libraries according to the specification given in a
configuration file.

Libraries meta data
-------------------

{
  "arc2" : {
      "summary":"php library to deal with RDF, RDF Store and SPARQL Endpoint",
      "github":"semsol/arc2",
      "language":"php",
      "workertime":"yes",
      "webtime":"yes",
      "updates":"automatic"
    },
  "php-github-api" : {
      "summary":"github API in php", 
      "github":"ornicar/php-github-api",
      "language":"php",      
      "workertime":"yes",
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
  "geshizip" : {
      "summary":"Just a test. The last version of geshi",
      "urls":{
        "http://sourceforge.net/projects/geshi/files/geshi/GeSHi%201.0.8.10/GeSHi-1.0.8.10.zip/download" : "GeSHi-1.0.8.10.zip"
        },
      "language":"zip",
      "workertime":"yes",
      "updates":"onlyOnce"
    },    
  "megalib" : { 
      "summary":"php library containing various helper class to deal with rdf, graphs, files, html, etc",
      "github":"megaplanet/megalib",
      "language":"php",      
      "workertime":"yes",
      "webtime":"yes",
      "updates":"automatic"      
    },
  "humanNameParser" : {
      "summary":"php library to parse human names",
      "github":"jasonpriem/HumanNameParser.php",
      "language":"php",
      "webtime":"yes",
      "updates":"automatic"
    },
  "snorql" : {
      "summary":"AJAXy front-end for exploring RDF SPARQL endpoints",
      "github":"kurtjx/SNORQL",
      "language":"javascript",
      "webtime":"yes",
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
