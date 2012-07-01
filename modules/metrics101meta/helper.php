<?php

$ifilename = $argv[1];
$ofilename = $argv[2];
$language = $argv[3];

define('_MEGALIB','true');
define('DEBUG',10);
define('ABSPATH_BASE',dirname(dirname(dirname(__DIR__))).'/');
define('ABSPATH_EXTERNAL_LIBRARIES',ABSPATH_BASE.'101results/libraries/');
define('ABSPATH_MEGALIB',ABSPATH_EXTERNAL_LIBRARIES.'megalib/');
define('ABSPATH_SRC_GESHI_LIBRARY',ABSPATH_EXTERNAL_LIBRARIES.'geshi/');

require_once ABSPATH_MEGALIB.'SourceCode.php';

$content = file_get_contents($ifilename);
$sc = new SourceCode($content,$language);
$summary = $sc->getSummary();
$metrics = array(
      'size'   => $summary['size'],
      'loc'    => $summary['nloc'],
      'ncloc'  => $summary['ncloc'] );
file_put_contents($ofilename, jsonEncode($metrics));
?>