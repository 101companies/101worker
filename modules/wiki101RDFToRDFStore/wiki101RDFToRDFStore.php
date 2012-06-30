<?php

require_once '../../configs/RDF101.config.php' ;

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

if (file_put_contents(RDF_STORE_END_POINT_CODE,$endPointCode)===false) {
  echo("Cannot create ".RDF_STORE_END_POINT_CODE);
  exit(3) ;
}
