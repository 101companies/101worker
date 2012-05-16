<?php
$thisScript=$argv[0];
$baseDirectory=$argv[1];
$targetDirectory=$argv[2];
$mainDirectory=$argv[3] ;


echo "Starting $thisScript $baseDirectory $targetDirectory $mainDirectory\n" ;
require_once '../../configs/main.config.local.php' ;
echo "Using megalib from ".ABSPATH_MEGALIB ;
require_once ABSPATH_MEGALIB.'SourceCode.php' ;
require_once ABSPATH_MEGALIB.'Files.php' ;

ini_set('memory_limit', '2048M');
$subdirectories = listAllFilesNames(addToPath($baseDirectory,$mainDirectory),'dir') ;
foreach ($subdirectories as $subdirectory) {
  $directoryToScan = addToPath($mainDirectory,basename($subdirectory)) ;
  echo "\n\n====== scanning $directoryToScan ================\n" ;
//  $srcdir = new SourceTopDirectory($baseDirectory,$directoryToScan) ;
//  $srcdir->generate($targetDirectory) ;
}

