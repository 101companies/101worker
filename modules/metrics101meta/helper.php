<?php

$input     = $argv[1];
$language  = $argv[2];
$relevance = $argv[3];


define('_MEGALIB', 'true');
define('DEBUG', 10);
define('ABSPATH_BASE', getenv('output101dir').'/');
define('ABSPATH_EXTERNAL_LIBRARIES', ABSPATH_BASE.'101results/libraries/');
define('ABSPATH_MEGALIB', ABSPATH_EXTERNAL_LIBRARIES.'megalib/');
define('ABSPATH_SRC_GESHI_LIBRARY', ABSPATH_BASE.'101results/geshi/src/');


require_once 'megalib_leftover.php';


$content = file_get_contents($input);
$sc      = new SourceCode($content, $language);
$summary = $sc->getSummary();
$result  = array(
    'metrics' => array(
        'size'      => $summary['size'],
        'loc'       => $summary['nloc'],
        'ncloc'     => $summary['ncloc'],
        'relevance' => $relevance,
    ),
    'tokens'  => $sc->getTokens(),
);

echo json_encode($result);
