<?php
$n=0 ;
$thisScript=$argv[$n++];
$sourceBaseDirectory=$argv[$n++];
$targetBaseDirectory=$argv[$n++];
$mainDirectory=$argv[$n++] ;
$sourceDirectoryMatchingRules=$argv[$n++] ;
$tmpDirectory=$argv[$n++] ;
$commandsBaseDirectory==$argv[$n++] ;
 

require_once '../../configs/main.config.local.php' ;
echo "Using megalib from ".ABSPATH_MEGALIB ;
require_once ABSPATH_MEGALIB.'Fragments.php' ;

echo "=== Creating the reader with rules from $sourceDirectoryMatchingRules\n" ;
$reader = new TaggedFragmentSetReader($sourceDirectoryMatchingRules) ;


$sourceDirectory=addToPath($sourceBaseDirectory,$mainDirectory) ;
echo "=== Reading tagged fragment definitions from $sourceDirectory\n" ;
$taggedFragmentSet = $reader->read($sourceDirectory) ;
$nbErrors = count($reader->getErrors()) ;
if ($nbErrors!==0) {
  echo "--> $nbErrors error(s) found\n" ;
  echo $reader->getErrorsAsJson(true) ;
  echo "\n" ;
}

if (DEBUG>10) echo htmlAsIs($taggedFragmentSet->asJson(true)) ;

echo "=== Applying locators to find fragment location\n" ;
$locatorIterator = new FragmentLocatorIterator($tmpDirectory,$commandsBaseDirectory) ;
$locatorIterator->addLocationToAllFragments($taggedFragmentSet,true) ;

echo "=== Computing derived informationn\n" ;
$taggedFragmentSet->computeDerivedInformation() ;
if (DEBUG>10) echo $taggedFragmentSet->asJson(true) ;



echo "=== Saving taggedFragments to json files\n" ;
$taggedFragmentSet->saveInJsonSummaryFiles($sourceBaseDirectory,$targetBaseDirectory,true) ;

echo "done" ;