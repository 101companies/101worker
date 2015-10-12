<?php

$ifilename = $argv[1];
$language  = $argv[2];
$factsfile = $argv[3];


define('_MEGALIB','true');
define('DEBUG',10);
define('ABSPATH_BASE', getenv('output101dir').'/');
define('ABSPATH_EXTERNAL_LIBRARIES',ABSPATH_BASE.'101results/libraries/');
define('ABSPATH_MEGALIB',ABSPATH_EXTERNAL_LIBRARIES.'megalib/');
define('ABSPATH_SRC_GESHI_LIBRARY',ABSPATH_EXTERNAL_LIBRARIES.'geshi/');

require_once 'megalib_leftover.php';


$factsfilecontent = file_get_contents($factsfile);
$facts            = json_decode($factsfilecontent, true);
$fragments        = $facts['fragments'];

$result = array(
    'metrics' => array(),
    'tokens'  => array(),
);


if($fragments) {
    $subfragments = array();
    getFragments($fragments, '', $subfragments);

    $lines = file($ifilename);

    foreach ($subfragments as $fragment => $lineRange) {
        $from    = $lineRange['startLine'];
        $to      = $lineRange[  'endLine'];
        $content = '';

        for ($i = $from - 1; $i < $to; $i++) {
               $content .= $lines[$i];
        }

        $tempresult = computeResults($content);
        $result['metrics'][$fragment] = $tempresult['metrics'];
        $result['tokens' ][$fragment] = $tempresult['tokens'];
    }
}


echo json_encode($result);



function computeResults($filecontent) {
    global $language, $relevance;

    $sc      = new SourceCode($filecontent, $language);
    $summary = $sc->getSummary();

    return array(
        'metrics' => array(
            'size'      => $summary['size'],
            'loc'       => $summary['nloc'],
            'ncloc'     => $summary['ncloc'],
            'relevance' => 'system',  # XXX: Why is this even necessary? The old
        ),                            # XXX: code had this, so I'm keeping it,
        'tokens' => $sc->getTokens(), # XXX: but it seems pretty silly.
    );
}


function getFragments($fragments, $parentName, &$subfragments) {

    foreach ($fragments as $fragment) {

        $index = '';
        if(array_key_exists('index', $fragment)) {
            $index .= "/$fragment[index]";
        }

        if(empty($parentName)){
            $fragmentName = "$fragment[classifier]/$fragment[name]$index";
        } else {
            $fragmentName = "$parentName/$fragment[classifier]/$fragment[name]$index";
        }

        if(array_key_exists('startLine', $fragment) && array_key_exists('endLine', $fragment)) {
            $lineRange = array(
                'startLine' => $fragment['startLine'],
                'endLine'   => $fragment[  'endLine'],
            );
            $subfragments[$fragmentName] = $lineRange;
        }

        if(array_key_exists('fragments', $fragment)) {
           getFragments($fragment['fragments'], $fragmentName, $subfragments);
        }
    }
}
