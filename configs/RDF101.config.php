<?php

require_once 'main.config.php' ;  

require_once ABSPATH_MEGALIB.'configs/RDF.config.php' ;

define('RDF_101_STORE_NAME','s101') ;

// information for the database containing the s101 rdf store

// schema file that is used by the converter json to rdf to select the
// information that will go in the rdf
define('WIKI_101_SCHEMA_URL','./Schema101.ss') ;

// mapping between entity kinds and top-level json tags
define('WIKI_101_ENTITY_JSON_MAPPING_URL','./EntityKind101ToJson101Tag.json') ;


define('RDF_DATA_101_PREFIX','d101') ;
define('RDF_DATA_101_PREFIX_URL',URL_PROJECT_101_URL.'/data/') ;

define('RDF_SCHEMA_101_PREFIX_URL',URL_PROJECT_101_URL.'/schema#') ;
define('RDF_SCHEMA_101_PREFIX','s101') ;

define('RDF_WIKI_101_NAMED_GRAPH',URL_PROJECT_101_URL.'/dumps/Wiki101Full.rdf') ;
define('RDF_CODE_101_NAMED_GRAPH',URL_PROJECT_101_URL.'/dumps/Repository101Full.rdf') ;
define('RDF_WIKI_101_DATA_GENERATED_CORE_FILENAME',ABSPATH_DATA_GENERATED.'Wiki101Full') ;

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
      RDF_DATA_101_PREFIX=>RDF_DATA_101_PREFIX_URL, 
      RDF_SCHEMA_101_PREFIX=>RDF_SCHEMA_101_PREFIX_URL) ;
  
  $configurationStore101 = new RDFStoreConfiguration(
      $prefixes101,
      $dbaccount, 
      RDF_101_STORE_NAME) ;
  return new RDFStore($configurationStore101) ;
}
