<?php
require_once '../../configs/main.config.local.php' ;
require_once ABSPATH_MEGALIB.'SourceCode.php' ;

$thisScript=$argv[0];
$baseDirectory=$argv[1];
$targetDirectory=$argv[2];
$directoryToScan=$argv[3];

$srcdir = new SourceDirectory($sourceDirectory,$directoryToScan) ;
$srcdir->generate(targetDirectory) ;