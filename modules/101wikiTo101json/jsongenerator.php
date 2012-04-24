<?php

define('BASE_PATH',str_replace('jsongenerator','',dirname(__FILE__)));
define('BASE101URL','http://101companies.org/index.php/');
error_reporting(E_ALL);
ini_set('display_errors','On');
require_once(BASE_PATH.'/../../libraries/MediaWikiAPI/ApiWrapper2.php');
require_once(BASE_PATH.'/../../libraries/MediaWikiAPI/ApiWrapper.php');

if(function_exists('lcfirst') === false) {
    function lcfirst($str) {
        $str[0] = strtolower($str[0]);
        return $str;
    }
}

// helper
function getNamespace($title){
  if(strpos($title,":") === FALSE)
  	return "";
  else 
  	return substr($title, 0, strpos($title,":"));
}

function pageJSON($title) {
  echo "Generating JSON for page \"".$title."\"... ";
  $page = new Page($title);
  $top = array();
  $top['name'] = $title;
  $top['type'] = 'Page';
  $top['url'] = BASE101URL.$title;
  $top['headline'] = $page->intent;
  if ($page->intent == null)
    $top['headline'] = "";
  $top['dicussion'] = $page->discussion;
  if ($page->dicussion == null)
      $top['dicussion'] = "";
  $result = array();
    $result['json'] = '$'.json_encode($top).'$';    
  echo "DONE".PHP_EOL;
    return $result;  
}

function concJSON($title) {
	echo "Generating JSON for concept or term \"".$title."\"... ";
	$page = new Page($title);
	$top = array();
  $top['name'] = $title;
  $top['type'] = 'Concept';
  $top['url'] = BASE101URL.$title;
  $top['headline'] = $page->intent;
  if ($page->intent == null)
  	$top['headline'] = "";
	$top['dicussion'] = $page->discussion;
	if ($page->dicussion == null)
  		$top['dicussion'] = "";
	$result = array();
  	$result['json'] = '$'.json_encode($top).'$';    
 	echo "DONE".PHP_EOL;
  	return $result;  
}

function catJSON($title, $subcs, $members) {
  $prefix2Type['Language'] = 'Language';
  $prefix2Type[''] = 'Concept';
  $prefix2Type['101feature'] = 'Feature';
  $prefix2Type['101implementation'] = "Implementation";
  $prefix2Type['Technology'] = 'Technology';
  $prefix2Type['Category'] = 'Category';
	echo "Generating JSON for category \"".$title."\"... ";
	$page = new Page("Category:".$title);
	$top = array();
  $top['name'] = $title;
  $top['type'] = 'Category';
  $top['url'] = BASE101URL.'Category:'.$title;
  $top['headline'] = $page->intent;
  if ($page->intent == null)
  		$top['headline'] = "";
	$top['dicussion'] = $page->discussion;
	if ($page->dicussion == null)
  		$top['dicussion'] = "";
  	$subs = array();
  	foreach($subcs as $sub){
  		$subo = array();
  		$subo['name'] = $sub;
  		array_push($subs, $subo);
  	}
	$top['categories'] = $subs;
	$mems = array();
  foreach ($prefix2Type as $prefix => $type) {
    $mems[$type] = array();
  }
	foreach($members as $member){  
    $curPrefix = getNamespace($member);
    $memo = array();
    $memo['name'] = $member;
    foreach($prefix2Type as $prefix => $type){
      if ($curPrefix == $prefix) {
        array_push($mems[$type], $memo);
      }
          
    }
	}
  foreach($mems as $type => $members){
    $top[$type.'Members'] = $members;  
  }
	
	$result = array();
  	$result['json'] = '$'.json_encode($top).'$';    
 	echo "DONE".PHP_EOL;
  	return $result;    
}

function implJSON($title,&$indexs){
  echo "Generating JSON for implementation \"".$title."\"... ";
  $page = new ImplementationPage("101implementation:".$title);
  $top = array();
  $top['name'] = $title;
  $top['type'] = 'Implementation';
  $top['url'] = BASE101URL.'101implementation:'.$title;  
  $top['headline'] = $page->intent;
  if($page->intent == null)
    $top['headline'] = "";
  $top['motivation'] = trim($page->motivation);
  $feats = array();
  $featIds = array();
  $missingFeats = array();
  foreach($page->getFeats() as $feat){
   	   $feato = array();
       $feato['name'] = '101feature:'.$feat;
       array_push($feats, $feato);
       if ( $indexs['101feature:'.$feat] == NULL) {
       	array_push($missingFeats, $feat);
        $indexs['101feature:'.$feat] = count($indexs);
       }
       array_push($featIds, $indexs['101feature:'.$feat]);
  }
  $top['features'] = $feats;
  
  $langs = array();
  $langIds = array();
  $missingLangs = array();
  foreach($page->getLangs() as $lang){
  	  $lango = array();
      $lango['name'] = 'Language:'.$lang;
      array_push($langs, $lango);
      if ($indexs['Language:'.$lang] == NULL) {
        array_push($missingLangs, $lang);
      	$indexs['Language:'.$lang] = count($indexs);
      }
   	   array_push($langIds, $indexs['Language:'.$lang]);
  }
  $top['languages'] = $langs;
  $techs = array();
  $techIds = array();
  $missingTechs = array();
  foreach($page->getTechs() as $tech){
      $techo = array();
      $techo['name'] = 'Technology:'.$tech;
      array_push($techs, $techo);
      if ($indexs['Technology:'.$tech] == NULL) {
      	array_push($missingTechs, $tech);
      	$indexs['Technology:'.$tech] = count($indexs);
      }
      array_push($techIds, $indexs['Technology:'.$tech]);
  }
  $top['technologies'] = $techs;
  if($page->illustration != "")
    $top['illustration'] = trim($page->illustration);
  if($page->architecture != "")
    $top['architecture'] = trim($page->architecture);
  if($page->usage != "")
    $top['usage'] = trim($page->usage);
  if($page->issues != "")
    $top['issues'] = trim($page->issues);  
  
      
  $result = array();
  $result['json'] = '$'.json_encode($top).'$';
  $result['feats'] = $feats;
  $result['langs'] = $langs;
  $result['techs'] = $techs; 
  $result['missingFeats'] = $missingFeats;
  $result['missingLangs'] = $missingLangs;
  $result['missingTechs'] = $missingTechs;
  echo "DONE".PHP_EOL;
  return $result;
}

function featJSON($title, $impltitles,$indexs){
  echo "Generating JSON for feature \"".$title."\"... ";
  $page = new FeaturePage("101feature:".$title);
  $top = array();
  $top['name'] = $title;
  $top['type'] = 'Feature';
  $top['url'] = BASE101URL.'101feature:'.$title;
  $top['headline'] = $page->intent;
  if($page->intent == null)
    $top['headline'] = "";
  if($page->description != "")
    $top['description'] = trim($page->description); 
  if($page->illustration != "")
    $top['illustration'] = trim($page->illustration);
  $impls = array();
  foreach($impltitles as $impltitle){
  	   $pair = array();
  	   $pair['name'] = $impltitle;
       array_push($impls, $pair);
  }
  $top['implementations'] = $impls;
  
  $result = array();
  $result['json'] = '$'.json_encode($top).'$';    
  echo "DONE".PHP_EOL;
  return $result;  
}



function langJSON($title, $impltitles,$indexs){
  echo "Generating JSON for language \"".$title."\"... ";
  $page = new LanguagePage("Language:".$title);
  $top = array();
  $top['name'] = $title;
  $top['type'] = 'Language';
  $top['url'] = BASE101URL.'Language:'.$title;
  $top['headline'] = $page->intent;
  if($page->intent == null)
    $top['headline'] = "";
  if($page->description != "")
    $top['description'] = trim($page->description); 
   $impls = array();
  foreach($impltitles as $impltitle){
  	   $pair = array();
  	   $pair['name'] = $impltitle;
       array_push($impls, $pair);
  }
  $top['implementations'] = $impls;
  
  $result = array();
  $result['json'] = '$'.json_encode($top).'$';    
  echo "DONE".PHP_EOL;
  return $result;  
}

function techJSON($title, $impltitles,$indexs){
  echo "Generating JSON for technology \"".$title."\"... ";
  $page = new TechnologyPage("Technology:".$title);
  $top = array();
  $top['name'] = $title;
  $top['type'] = 'Technology';
  $top['url'] = BASE101URL.'Technology:'.$title;
  $top['headline'] = $page->intent;
  if($page->intent == null)
    $top['headline'] = "";
  if($page->description != "")
    $top['description'] = trim($page->description); 
    $impls = array();
  foreach($impltitles as $impltitle){
  	   $pair = array();
  	   $pair['name'] = $impltitle;
       array_push($impls, $pair);
  }
  $top['implementations'] = $impls;
  
  $result = array();
  $result['json'] = '$'.json_encode($top).'$';    
  echo "DONE".PHP_EOL;
  return $result;  
}

function emptyJSON($title, $type, $impltitles, $indexs){
  $prefixs['feature'] = "101feature";
  $prefixs['language'] = "Language";
  $prefixs['technology'] = "Technology";
  echo "Generating empty JSON for ".$type." \"".$title."\"... ";
  $top = array();
  $top['name'] = $title;
  $top['type'] = ucfirst($type);
  $top['url'] = $indexs[$prefixs[$type].':'.$title];
  $top['headline'] = "";
  $impls = array();
  foreach($impltitles as $impltitle){
      array_push($impls, $indexs['101implementation:'.$impltitle]);
  }
  $top['implementations'] = $impls;
  
  $wrapper = array();
  $wrapper['op'] = "insert";
  $prefixs = array();
  $wrapper['id'] = $indexs[$prefixs[$type].':'.$title];
  $wrapper['type'] = "technology";  
  $wrapper['entry'] = $top;
  
  $result = array();
  $result['json'] = '$'.json_encode($wrapper).'$';    
  echo "DONE".PHP_EOL;
  return $result;  
 
}

function saveJSON($title, $jsons){
  #$file = fopen('./data/'.$title.'.json','w+');
  $pattern = array(',"', '${', '}$','},{');
  $replacement = array(",\n\t\"", "{\n\t", "\n}","},\n\t\t{"); 
  $texts = array();
  foreach($jsons as $name => $json){
    array_push($texts, '"'.$name.'" : '.str_replace($pattern, $replacement, $json));
  }
  #fwrite($file, '['.PHP_EOL.implode(','.PHP_EOL, $texts).PHP_EOL.']');
  #fclose($file);
  return '{'.PHP_EOL.implode(','.PHP_EOL, $texts).PHP_EOL.'}';

}

// check for path information
if (count($argv) <= 1)
  exit("Need output path for json result\n");
// MAIN
$allPages = getAllPages();
$indexs = array();
for($i = 0; $i < count($allPages); $i++){
 $page = $allPages[$i];
 $title = $page['title'];
 $indexs[$title] = $i;
}
var_dump($indexs);
//sleep(5);
$all = "{";
$nss = array();
$conctitles = array();
$cattitles = array();
$impltitles = array();
$feattitles = array();
$langtitles = array();
$techtitles = array();
$pagetitles = array();
foreach($allPages as $page) {
  $s = getPage($page['title']);
  if ($s == null or startsWith("#REDIRECT", $s))
    continue;
  $namespace = getNamespace($page['title']);
  if(!in_array($namespace,$nss)){
    array_push($nss, $namespace);
  }
  $title = str_replace($namespace.':', "", $page['title']);
  $json = "{".PHP_EOL;
  switch($namespace){
  	case "":
  	  array_push($conctitles, $title);
  	  break;
    case "101implementation":                                                                                                                                                                                 
      array_push($impltitles, $title);
      break;
    case "101feature":                                                                                                                                                                             
      array_push($feattitles, $title);
      break;
    case "Language":                                                                                                                                                                             
      array_push($langtitles, $title);
      break;
    case "Technology":                                                                                                                                                                             
      array_push($techtitles, $title);
      break;  
    default:
      array_push($pagetitles, $page['title']);
      break;   
  }
}
var_dump($conctitles);
$ontology = getOntology();
var_dump($ontology);
$coverage = array();
$languse = array();
$techuse = array();
$jsons = array();
$missing = array();
$implj = array();
$fti = array();
foreach($impltitles as $impltitle){
   $result = implJSON($impltitle,$indexs);
   array_push($jsons, $result['json']);
   #array_push($implj, $result['json']);
   $implj[$impltitle] = $result['json'];
   array_push($fti, $impltitle);
   foreach($result['feats'] as $feato){
     $feat = $feato['name'];
     if (array_key_exists($feat, $coverage))
      array_push($coverage[$feat], $impltitle);
     else
      $coverage[$feat] = array($impltitle);
   }
   foreach($result['langs'] as $lango){
     $lang = $lango['name'];
     if (array_key_exists($lang, $languse))
      array_push($languse[$lang], $impltitle);
     else
      $languse[$lang] = array($impltitle);
   }
   foreach($result['techs'] as $techo){
     $tech = $techo['name'];
     if (array_key_exists($tech, $techuse))
      array_push($techuse[$tech], $impltitle);
     else
      $techuse[$tech] = array($impltitle);
   }
   foreach($result['missingFeats'] as $missingFeat){
   	$misso = array();
   	$misso['type'] = 'feature';
   	$misso['name'] = $missingFeat;
   	array_push($missing,$misso);
   }
   foreach($result['missingLangs'] as $missingLang){
   	$misso = array();
   	$misso['type'] = 'language';
   	$misso['name'] = $missingLang;
   	array_push($missing,$misso);
   }
   foreach($result['missingTechs'] as $missingTech){
   	$misso = array();
   	$misso['type'] = 'technology';
   	$misso['name'] = $missingTech;
   	array_push($missing,$misso);
   }
}
#$all .= '"ImplementationMembers":'. json_encode($fti).PHP_EOL.','.PHP_EOL;
$all .= '"Implementation":'. saveJSON('implementation', $implj).PHP_EOL.','.PHP_EOL;
var_dump($missing);

$pagej = array();
$ftpa = array();
foreach($pagetitles as $pagetitle) {
  $result = pageJSON($pagetitle);
  array_push($jsons, $result['json']);
  $pagej[$pagetitle] = $result['json'];
  array_push($ftpa, $pagetitle);
}
#$all .= '"ConceptMembers":'. json_encode($ftco).PHP_EOL.','.PHP_EOL;
$all .= '"Page":'. saveJSON('pagetitle', $pagej).PHP_EOL.','.PHP_EOL;

$concj = array();
$ftco = array();
foreach($conctitles as $conctitle) {
  $result = concJSON($conctitle);
  array_push($jsons, $result['json']);
  #array_push($concj, $result['json']);
  $concj[$conctitle] = $result['json'];
  array_push($ftco, $conctitle);
}
#$all .= '"ConceptMembers":'. json_encode($ftco).PHP_EOL.','.PHP_EOL;
$all .= '"Concept":'. saveJSON('concept', $concj).PHP_EOL.','.PHP_EOL;

$catj = array();
$ftca = array();
foreach($ontology as $x => $info) {
  $result = catJSON($x, $info['categories'], $info['members']);
  array_push($jsons, $result['json']);
  #array_push($catj, $result['json']);
  $catj[$x] = $result['json'];
  array_push($ftca, $x);
}
#$all .= '"CategoryMembers":'. json_encode($ftca).PHP_EOL.','.PHP_EOL;
$all .= '"Category":'. saveJSON('category', $catj).PHP_EOL.','.PHP_EOL;

$featj = array();
$ftf = array();
foreach($feattitles as $feattitle){
  $result = featJSON($feattitle, $coverage[lcfirst($feattitle)],$indexs);
  array_push($jsons, $result['json']);
  #array_push($featj, $result['json']);
  $featj[$feattitle] = $result['json'];
  array_push($ftf, $feattitle);
}
#$all .= '"FeatureMembers":'. json_encode($ftf).PHP_EOL.','.PHP_EOL;
$all .= '"Feature":'. saveJSON('feature', $featj).PHP_EOL.','.PHP_EOL;
$langj = array();
$ftl = array();
foreach($langtitles as $langtitle){
  $result = langJSON($langtitle, $languse[$langtitle],$indexs);
  array_push($jsons, $result['json']);
  #array_push($langj, $result['json']);
  $langj[$langtitle] = $result['json'];
  array_push($ftl, $langtitle);
}
#$all .= '"LanguageMembers":'. json_encode($ftl).PHP_EOL.','.PHP_EOL;
$all .= '"Language":'. saveJSON('language', $langj).PHP_EOL.','.PHP_EOL;
$techj = array();
$ftt = array();
foreach($techtitles as $techtitle){
  $result = techJSON($techtitle, $techuse[$techtitle],$indexs);
  array_push($jsons, $result['json']);
  #array_push($techj, $result['json']);
  $techj[$techtitle] = $result['json'];
  array_push($ftt, $techtitle);
}
#$all .= '"TechnologyMembers":'. json_encode($ftt).PHP_EOL.','.PHP_EOL;
$all .= '"Technology":'. saveJSON('technology', $techj).PHP_EOL.PHP_EOL.'}'.PHP_EOL;
foreach($missing as $m){
  switch ($m['type']) {
	case "feature":
		$impls = $coverage[lcfirst($m['name'])];
		break;
	case "language":
		$impls = $languse[$m['name']];
		break;
	case "technology":
		$impls = $techuse[$m['name']];
		break;	  
  }
  $result = emptyJSON($m['name'],$m['type'],$impls,$indexs);
  array_push($jsons, $result['json']);
}
#saveJSON('101knowledge', $jsons);
$file = fopen($argv[1],'w+');
fwrite($file, $all);
fclose($file);

echo "Detected namespaces:".PHP_EOL;
var_dump($nss);
echo "ALL DONE".PHP_EOL;






