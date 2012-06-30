<?php
require_once '../../configs/RDF101.config.php' ;

if (count($argv)!==2) {
  echo "usage: <pathOfSparql.php>" ;
  exit(2) ;
}
echo "====== Deploying the end point code to ".$argv[1]." =========\n" ;
$endPointCode =
  '<?php
   require_once("../101woxxxrker/configs/RDF101.config.php") ;
   get101Store()->startSparqlEndpoint() ;
  ' ;   

if (file_put_contents($argv[1],$endPointCode)===false) {
  echo("Cannot create ".$argv[1]);
  exit(3) ;
}
