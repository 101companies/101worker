<?php
$thisScript=$argv[0];
$baseDirectory=$argv[1];
$targetDirectory=$argv[2];
$mainDirectory=$argv[3] ;


echo "Starting $thisScript $baseDirectory $targetDirectory $mainDirectory\n" ;
require_once '../../configs/main.config.local.php' ;
echo "Using megalib from ".ABSPATH_MEGALIB ;
require_once ABSPATH_MEGALIB.'Files.php' ;
require_once ABSPATH_MEGALIB.'SourceCode.php' ;
require_once ABSPATH_MEGALIB.'SourceFileSystem.php' ;

echo 'WARNING: this script generates all source codes.'."\n"
echo '         Because of php poor memory managment, out of memory might occur.'."\n" ;
echo '         In this case change the value of $scanPerSubdirectories in '.__FILE__."\n" ;

$scanPerSubdirectories = false ;
ini_set('memory_limit', '2048M');

if ($scanPerSubdirectories) {
  $subdirectories = listFileNames(addToPath($baseDirectory,$mainDirectory),'dir') ;
  foreach ($subdirectories as $subdirectory) {
    $directoryToScan = addToPath($mainDirectory,basename($subdirectory)) ;
    echo "\n\n====== scanning $directoryToScan ================\n" ;
    $srcdir = new SourceTopDirectory($baseDirectory,$directoryToScan) ;
    $srcdir->generate($targetDirectory) ;
  }
} else {
  $srcdir = new SourceTopDirectory($baseDirectory,$mainDirectory) ;
  $srcdir->generate($targetDirectory) ;
}

