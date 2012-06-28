<?php
define('BASE_PATH',str_replace('jsongenerator','',dirname(__FILE__)));
require_once(BASE_PATH.'/../../libraries/MediaWikiAPI/ApiWrapper.php');
require_once(BASE_PATH.'/../../libraries/MediaWikiAPI/Pages.php');


 // check for path information
if (count($argv) <= 1)
  exit("Need output path for XML result\n");

$pages = getAllPages();
$pagetitles = array();
$map = array();
echo "Scanning pages...\n";
foreach($pages as $page) {
	$title = $page['title'];
	array_push($pagetitles, $title);
	if (strstr(getPageContent($title), "<classify/>") !== FALSE)
		$map[str_replace(" ", "_", $title)] = array("classify" => TRUE);
}	

echo "Requesting categories...\n";
$categories = getCategories();
$classifycats = array();
foreach($categories as $category){
	if (strstr($category, "<pageheadline/>") !== FALSE) {
		if (!array_key_exists($category, $map)) {
			$map[str_replace(" ", "_", $category)] = array("pageheadline" => TRUE);
		} else {
			$map[str_replace(" ", "_", $category)]["pageheadline"] = TRUE;
		}
		
	}
}
echo json_decode($map);
$handle = fopen ($argv[1], "w");
fwrite($handle, json_encode($map));
fclose($handle);
?>