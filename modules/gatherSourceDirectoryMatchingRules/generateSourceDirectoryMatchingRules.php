<?php
$n=0 ;
$thisScript=$argv[$n++];
$sourceRuleFile=$argv[$n++] ;
$targetRuleFile=$argv[$n++] ;

require_once '../../configs/main.config.local.php' ;
echo "Using megalib from ".ABSPATH_MEGALIB."\n" ;
require_once ABSPATH_MEGALIB.'CSV.php' ;
require_once ABSPATH_MEGALIB.'Files.php' ;

echo "loading source rule file from $sourceRuleFile\n" ;
$csv = new CSVFile() ;
if (!$csv->load($sourceRuleFile)) {
  die("File $sourceRuleFile not found\n") ;
}
echo "saving the rule file to $targetRuleFile\n" ;
if(!saveFile($targetRuleFile,$csv->getJSON())) {
  die('Cannot save file '.$targetRuleFile."\n") ;
}
echo "done" ;

