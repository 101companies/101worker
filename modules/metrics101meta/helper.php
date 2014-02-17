<?php

// TODO: no comments: https://github.com/megaplanet/megalib/blob/master/SourceCode.php#L914-L920

$ifilename = $argv[1];
$ofilename1 = $argv[2];
$ofilename2 = $argv[3];
$language = $argv[4];
$relevance = $argv[5];
$factsfile = $argv[6];  // Maybe feed this file per standard in ?

define('_MEGALIB','true');
define('DEBUG',10);
define('ABSPATH_BASE',dirname(dirname(dirname(__DIR__))).'/');
define('ABSPATH_EXTERNAL_LIBRARIES',ABSPATH_BASE.'101results/libraries/');
define('ABSPATH_MEGALIB',ABSPATH_EXTERNAL_LIBRARIES.'megalib/');
define('ABSPATH_SRC_GESHI_LIBRARY',ABSPATH_EXTERNAL_LIBRARIES.'geshi/');

require_once 'megalib_leftover.php';

$content = '';
$result = array();

if( count($argv) > 6 ) {   // This is the case in which metrics for fragments should be computed

    $result['metrics'] = array();
    $result['tokens'] = array();

    $factsfilecontent = file_get_contents($factsfile);
    $facts = json_decode($factsfilecontent, true);
    $fragments = $facts['fragments'];

    if(empty($fragments) == false) {

    $subfragments = array();
    getFragments($fragments, '', $subfragments);

    $lines = file($ifilename);

    foreach ($subfragments as $fragment => $lineRange) {
	$from = $lineRange->{'startLine'};
        $to = $lineRange->{'endLine'};
	$content = '';

	for ($i = $from-1; $i < $to; $i++) {
   	    $content .= $lines[$i];
	}
        $tempresult = computeResults($content);
        $result['metrics'][$fragment] = $tempresult['metrics'];
        $result['tokens'][$fragment] = $tempresult['tokens'];   
    }
    }
} 

else {    // This is the case where metrics should be computed just for the whole file
	$content = file_get_contents($ifilename);
	$result = computeResults($content);
}

file_put_contents($ofilename1, json_encode((object) $result['metrics']));
file_put_contents($ofilename2, json_encode((object) $result['tokens']));


function computeResults($filecontent) {

    global $language, $relevance;

    $sc = new SourceCode($filecontent,$language);
    $summary = $sc->getSummary();

    $metrics = array(
	'size'   => $summary['size'],
	'loc'    => $summary['nloc'],
	'ncloc'  => $summary['ncloc'],
	'relevance' => $relevance );

    $tokens = $sc->getTokens();

    $result = array(
	'metrics'   => $metrics,
	'tokens'    => $tokens);
	
    return $result ;
}

function getFragments($fragments, $parentName, &$subfragments) {

    foreach ($fragments as $fragment) {
	$index = '';
	if(array_key_exists('index', $fragment)) {
           $index .= '/'.$fragment['index'];
        }
	if(empty($parentName) == true){
	    $fragmentName = $fragment['classifier'].'/'.$fragment['name'].$index;
	} else {
	    $fragmentName = $parentName.'/'.$fragment['classifier'].'/'.$fragment['name'].$index;
	}
	if(array_key_exists('startLine', $fragment) && array_key_exists('endLine', $fragment)) {
           $lineRange = array('startLine' => $fragment['startLine'],
			      'endLine' => $fragment['endLine']);

	   $subfragments[$fragmentName] = $lineRange;
        }
	if(array_key_exists('fragments', $fragment)) {
           getFragments($fragment['fragments'], $fragmentName, $subfragments);
        }
    }
}


?>
