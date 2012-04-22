<?php
define('BASE_PATH',str_replace('jsongenerator','',dirname(__FILE__)));
require_once(BASE_PATH.'/../../libraries/MediaWikiAPI/ApiWrapper.php');
require_once(BASE_PATH.'/../../libraries/MediaWikiAPI/Pages.php');

 
 
 function addNode(&$parent, $cat, $ontology) {
 	print "Adding category ".$cat."\n";
 	$catNode = $parent->addChild("cat");
 	$catNode->addAttribute("name", "Category:".$cat);
 	$p = new Page("Category:".$cat);
 	$subcats = $ontology[$cat]['categories'];
 	$catNode->addAttribute("intent", $p->intent);
 	foreach ($subcats as $subcat) {
 		$title = preg_replace("/Category:(.*)/", "$1", $subcat);
 		addNode($catNode, $title, $ontology);
 	}
 	$members = $ontology[$cat]['members'];
 	foreach($members as $member) {
 		print "Adding page ".$member."\n";
 		$pageNode = $catNode->addChild("page");
		$pageNode->addAttribute("name", $member);
		$page = new Page($member);
		$pageNode->addAttribute("intent", $page->intent);
 	}
 }

 // check for path information
if (count($argv) <= 1)
  exit("Need output path for XML result\n");
 
$handle = fopen ($argv[1], "w");
fwrite($handle, '<?xml version="1.0" encoding="utf8"?>');
fwrite($handle, '<cat name="Category:Base"></cat>');
fclose($handle);

$xml = simplexml_load_file($argv[1]);
print "Requesting ontology...";
$ontology = getOntology();
var_dump($ontology);
$subcats = $ontology['Base']['categories'];
foreach($subcats as $subcat){
    $title = preg_replace("/Category:(.*)/", "$1", $subcat);
 	addNode($xml, $title, $ontology);
 }
 
$handle = fopen($argv[1], "wb"); 
fwrite($handle, $xml->asXML());
fclose($handle);

?>