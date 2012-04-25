<?php
require_once 'main.config.php' ;  
require_once ABSPATH_MEGALIB.'configs/RDF.config.php' ;

define('RDF_101_STORE_NAME','s101') ;

define('DOMAIN_DATA_101','data'.DOMAIN_PROJECT_101) ;
define('RDF_DATA_101_URL','http://'.DOMAIN_DATA_101.'/data/') ;

define('RDF_DATA_101_PREFIX','d101') ;
define('RDF_DATA_101_URI_PATTERN',RDF_DATA_101_URL.'${type}/${id}') ;

define('RDF_SCHEMA_101_PREFIX','s101') ;
define('RDF_SCHEMA_101_PREFIX_URL',RDF_DATA_101_URL.'/schema#') ;


define('RDF_WIKI_101_NAMED_GRAPH',RDF_DATA_101_URL.'dumps/Wiki101Full.rdf') ;
define('RDF_CODE_101_NAMED_GRAPH',RDF_DATA_101_URL.'dumps/Repo101Full.rdf') ;

define ('RDF_STORE_END_POINT_CODE',ABSPATH_DATA_GENERATED.'sparql.php') ;
 
require_once ABSPATH_MEGALIB.'RDF.php' ;


/**
 * Return the 101 store.
 * This function should execute with no error if the database is set properly.
 * @return RDFStore!
 */

function get101Store() {
  $dbaccount = new DatabaseAccount(
      RDF_101_PRODUCTION_DATABASE_NAME,
      RDF_101_PRODUCTION_DATABASE_USER,
      RDF_101_PRODUCTION_DATABASE_PASSWORD) ;
  
  // define the prefixes available in SPARQL endpoint for instance
  $prefixes101 = array (
      RDF_SCHEMA_101_PREFIX=>RDF_SCHEMA_101_PREFIX_URL) ;
  
  $configurationStore101 = new RDFStoreConfiguration(
      $prefixes101,
      $dbaccount, 
      RDF_101_STORE_NAME) ;
  return new RDFStore($configurationStore101) ;
}
