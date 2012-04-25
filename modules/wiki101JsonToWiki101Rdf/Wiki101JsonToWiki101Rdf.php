<?php

require_once '../../configs/RDF101.config.php' ;
require_once ABSPATH_MEGALIB.'JsonGraphAsERGraph.php' ;
require_once ABSPATH_MEGALIB.'ERGraphAsRDF.php' ;
require_once ABSPATH_MEGALIB.'HTML.php' ;

$graph = jsonGraphToERGraph(
            URL_WIKI_101_JSON_URL,
            WIKI_101_SCHEMA_URL,
            WIKI_101_ENTITY_JSON_MAPPING_URL) ;

$graphasrdf = new ERGraphAsRDF() ;
$graphasrdf->addERGraph(
    $graph,RDF_DATA_101_URI_PATTERN,RDF_SCHEMA_101_PREFIX_URL) ;

// Save the triples in different file formats
if (DEBUG) echo "======= Saving the triples in files =========\n" ;
$tripleset = $graphasrdf->getTripleSet() ;
$formats='HTML,GraphML,Graphviz,Turtle,RDFXML,RDFJSON,NTriples' ;
$tripleset->saveFiles($formats,RDF_WIKI_101_DATA_GENERATED_CORE_FILENAME) ;



if (DEBUG) echo "======= Saving the triples in the RDF store ========\n" ;
// Save the triples in the RDF101 store
$store101 = get101Store() ;
//$store101->reset() ;
$graphasrdf->save($store101,RDF_WIKI_101_NAMED_GRAPH) ;


if (DEBUG) echo "====== Deploying the end point code to ".RDF_STORE_END_POINT_CODE." =========\n" ;
$endPointCode =
  '<?php
   require_once("../101worker/configs/RDF101.config.php") ;
   get101Store()->startSparqlEndpoint() ;
  ' ;   
file_put_contents(RDF_STORE_END_POINT_CODE,$endPointCode) ;

