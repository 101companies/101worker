<?php

require_once '../../configs/RDF101.config.php' ;

if (count($argv)!==2) {
  echo "usage: <nameOfFile>" ;
  exit(2) ;
}

$file = $argv[1] ;
$file = realpath($file) ;
echo "======= Loading the triples from $file ========\n" ;
$tripleset = new RDFTripleSet() ;
if (is_file($file)) {
  echo "File exists\n" ;
} else {
  echo "The file $file does not exists\n" ;
  exit(3) ;
}
$n = $tripleset->load("file:".$file) ;
if ($n===false) {
  echo "ERROR: Cannot read file $file\n" ;
  exit (4) ;
}
echo "$n tuples read\n" ;
 
echo "======= Loading the triples into the RDF store ========\n" ;
$store101 = get101Store() ;
$store101->loadTripleSet($tripleset,RDF_WIKI_101_NAMED_GRAPH) ;
