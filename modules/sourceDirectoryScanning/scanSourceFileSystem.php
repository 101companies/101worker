<?php
$n=0 ;
$thisScript=$argv[$n++];
$baseDirectory=$argv[$n++];
$targetBaseDirectory=$argv[$n++];
$mainDirectory=$argv[$n++] ;
$sourceDirectoryMatchingRules=$argv[$n++] ;
$sourceDirectoryScanningMethod=$argv[$n++] ;

echo "Starting $thisScript $baseDirectory $targetBaseDirectory $mainDirectory $sourceDirectoryMatchingRules $sourceDirectoryScanningMethod\n" ;
require_once '../../configs/main.config.local.php' ;
echo "Using megalib from ".ABSPATH_MEGALIB ;
require_once ABSPATH_MEGALIB.'Files.php' ;
require_once ABSPATH_MEGALIB.'SourceCode.php' ;
require_once ABSPATH_MEGALIB.'SourceFileSystem.php' ;
require_once ABSPATH_MEGALIB.'FileSystemMatcher.php' ;

$sourceDirectoryScanningMethod = false ;
ini_set('memory_limit', '2048M');

echo "WARNING: this script is eager in term of memory.\n" ;
echo "         Because of php poor memory managment, out of memory errors might occur.\n" ;
echo "         In this case change the value of sourceDirectoryScanningMethod in Makefile.var to 'perSubDirectories' \n" ;

echo "" ;
echo "sourceDirectoryScanningMethod=$sourceDirectoryScanningMethod\n" ;
echo "sourceDirectoryMatchingRules=$sourceDirectoryMatchingRules\n" ;
$matcher = new RuleBasedFileSystemPatternMatcher($sourceDirectoryMatchingRules) ;
echo $matcher->getRulesNumber()." rules where found." ;
echo "In this module rules are particularily important to define the 'elementKind' and 'geshiLanguage' properties " ;
if ($sourceDirectoryScanningMethod==='full') {
  echo "Scanning the whole directory $mainDirectory at once.\n" ;
  $actualTargetDirectory = addToPath($targetBaseDirectory,$mainDirectory) ;
  echo "this has the benefit of generating top level summary in $actualTargetDirectory\n" ;
  $srcdir = new SourceTopDirectory($baseDirectory,$mainDirectory,array(),$matcher) ;
  echo "generating the result in $actualTargetDirectory\n" ;
  $srcdir->generate($actualTargetDirectory)) ;
} else {
  $subdirectories = listFileNames(addToPath($baseDirectory,$mainDirectory),'dir') ;
  echo "Scanning all ".count($subdirectories)." subdirectories one by one.\n" ;  
  foreach ($subdirectories as $subdirectory) {
    $directoryToScan = addToPath($mainDirectory,basename($subdirectory)) ;
    $actualTargetDirectory = addToPath($targetBaseDirectory,$directoryToScan ;
    echo "\n\n====== scanning subdirectory $directoryToScan ================\n" ;
    $srcdir = new SourceTopDirectory($baseDirectory,$directoryToScan,array(),$matcher) ;
    echo "generating the result in $actualTargetDirectory\n" ;
    $srcdir->generate($actualTargetDirectory) ;
  }
} 
echo "generation was successfull\n" ;
