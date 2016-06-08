<?php

require_once '../../configs/RDF101.config.php' ;
require_once ABSPATH_MEGALIB.'JsonGraphAsERGraph.php' ;
require_once ABSPATH_MEGALIB.'ERGraphAsRDF.php' ;
require_once ABSPATH_MEGALIB.'HTML.php' ;

$corefilename=$argv[1] ;
$schemafile=$argv[2] ;

$graph = jsonGraphToERGraph($corefilename.'.json',$schemafile) ;

$graphasrdf = new ERGraphAsRDF() ;
$graphasrdf->addERGraph(
    $graph,RDF_DATA_101_URI_PATTERN,RDF_SCHEMA_101_PREFIX_URL) ;

// Save the triples in different file formats
if (DEBUG) echo "======= Saving the triples in files =========\n" ;
$tripleset = $graphasrdf->getTripleSet() ;
$formats='HTML,GraphML,Graphviz,Turtle,RDFXML,RDFJSON,NTriples' ;
$tripleset->saveFiles($formats,$corefilename) ;



