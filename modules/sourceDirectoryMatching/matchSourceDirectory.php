<?php
$n=0 ;
$thisScript=$argv[$n++];
$rulesFile=$argv[$n++];
$baseDirectory=$argv[$n++];
$targetDirectory=$argv[$n++];
$mainDirectory=$argv[$n++] ;
$rulesFile=$argv[$n++] ;

require_once '../../configs/main.config.local.php' ;
echo "Using megalib from ".ABSPATH_MEGALIB ;
require_once ABSPATH_MEGALIB.'SourceCode.php' ;

echo "Loading the rules from $rulesFile\n" ; ;
$json = file_get_content($rulesFile) ;
if ($json === false) {
  die("cannot open $rulesFile") ;
}
$rules = json_decode($json) ;
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
$resultDir = addToPath($targetDirectory,$mainDirectory) ;

echo "match directory $sourceDir and generate results in $resultDir\n" ;
$matcher->generate($sourceDir,$resultDir,$matchedFilesGrouping,array('language','technology')) ;
echo "done" ;



