<?php
$n=0 ;
error_reporting(E_ALL);

$thisScript=$argv[$n++];
$rulesFile=$argv[$n++];
$baseDirectory=$argv[$n++];
$targetDirectory=$argv[$n++];
$mainDirectory=$argv[$n++] ;

require_once '../../configs/main.config.local.php' ;
echo "Using megalib from ".ABSPATH_MEGALIB."\n" ;
require_once ABSPATH_MEGALIB.'SourceCode.php' ;
require_once ABSPATH_MEGALIB.'Structures.php' ;


echo "Loading the rules from $rulesFile\n" ; ;
$json = file_get_contents($rulesFile) ;
if ($json === false) {
  die("cannot open $rulesFile") ;
}
$rules = jsonDecodeAsMap($json) ;
echo "they are ".count($rules)." rules\n" ;

$matcher = new FileSystemPatternMatcher($rules) ;
$matchedFilesGrouping=array(
    'languages' => 
       array(
           'select' => array('locator','geshiLanguage'),
           'groupedBy' => 'language' 
        ),
     'technologies' =>
       array(
           'select' => array('role'),
           'groupedBy' => 'technology'
       )
 ) ;
$sourceDir = addToPath($baseDirectory,$mainDirectory) ;
$resultDir = addToPath(addToPath($targetDirectory,$mainDirectory),'.rulesMatches') ;

echo "match directory $sourceDir and generate results in $resultDir\n" ;
$matcher->generate($sourceDir,$resultDir,$matchedFilesGrouping,array('language','technology')) ;
echo "done" ;



