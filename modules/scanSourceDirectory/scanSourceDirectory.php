<?php
$thisScript=$argv[0];
$baseDirectory=$argv[1];
$targetDirectory=$argv[2];
$directoryToScan=$argv[3];

echo "Starting $thisScript $baseDirectory $targetDirectory $directoryToScan\n" ;
require_once '../../configs/main.config.local.php' ;
echo "Using megalib from ".ABSPATH_MEGALIB ;
require_once ABSPATH_MEGALIB.'SourceCode.php' ;

$srcdir = new SourceTopDirectory($baseDirectory,$directoryToScan) ;
$srcdir->generate($targetDirectory) ;