API/Pages.php<?php
define('BASE_PATH',str_replace('API','',dirname(__FILE__)));
require_once('ApiWrapper.php' );
require_once('Utils.php');

function extractBibs(&$content) {
  $bibs = array();
  $currentTag = '';
  $currentBib = '';
  $newContent = '';
  $inRefs = false;
  foreach(preg_split( '/\r\n|\r|\n/', $content) as $line) {
    if (startsWith("==References==",str_replace(' ','',trim($line)) )) {
        $inRefs= true;
        continue;
    }
    if (startsWith("==",trim($line))) {
        $inRefs = false; ;
    }
    // only non-bib content should be actual content
    if (!$inRefs){
      $newContent .= $line.PHP_EOL;
    }
    if ($inRefs) {
      if ('' == trim($line) || startsWith('<biblio>',trim($line)) || startsWith('</biblio>',trim($line)) )
        continue;
      preg_match_all('/#(.*)\s*bibtex=/',trim($line),$out);
      // new bib
      if(count($out[1])!= 0) {
        if ($currentTag != '') {
          $bibs[$currentTag] = $currentBib;
          $currentBib = '';
        }
        $currentTag = trim($out[1][0]);
        $line = str_replace($out[0],'',$line);
      }
      $currentBib .= $line.PHP_EOL;
    }
     
  }
  if ($currentTag != '') {
    $bibs[$currentTag] = $currentBib;
  }
  $content = $newContent;
  return $bibs;
  
  
}

function extractIntent($content) {
    $inIntent= false;
    $indent = "";
    foreach(preg_split( '/\r\n|\r|\n/', $content) as $line) {
      if (startsWith("==Intent==",str_replace(' ','',trim($line)) )) {
        $inIntent= true;
        continue;
      }
      if (startsWith("==",trim($line))) {
         $inIntent = false;
         continue;
      }
      if($inIntent) {
          if ($line != '') {
          	$intent = $line;
          	break;
          }
      }
    }
    
    return $intent;
}

function until($pattern,$text){
  if(strpos($text,$pattern) === FALSE)
  	return $text;
  else 
  	return substr($text, 0, strpos($text,$pattern));
}
                                                                                                            
function extractContent($content, $pattern){
  $inside = false;
  $res = "";
  $content = preg_split( '/\r\n|\r|\n/', $content);
  $preLine = '';
  foreach($content as $line) {
    //echo  PHP_EOL . $line . PHP_EOL;
    if($inside) {
     if (($line != '') && (startsWith("==", str_replace(' ','',$line))) && !(startsWith("===", str_replace(' ','',$line)))){ //next section begins
      $inside = false;
      break;    
     }
     
     if ($line == '' && !startsWith("</syntax",$preLine)) {
      $res .= PHP_EOL;
     }
     
     if ($line != '') { //we don't include empty lines
       $res .= PHP_EOL .$line;
     }     
    }
    if($inside == false){ //we're not inside the section yet
     if (startsWith($pattern, str_replace(' ','',trim($line)) )) {
      $inside = true;
     }  
   }
  $preLine = $line;
  }
  //ECHO "extract content for " . $pattern . var_dump($res);
  return $res;
}

class Page{
 private $title;
 public $content;
 public $intent;
 public $namespace;
 private $sections;
 public $rawDump;
 public $discussion;
 public $description;
 public $technologies;
 public $lastrev;
 public $creation;
 public $bibs;
 public $objective;
 
 function getTitle(){
  if(strpos($this->title,":") === FALSE)
  	return $this->title;
  else 
  	return substr($this->title, strpos($this->title,":")+1);
  // could still be usefull
  if(startsWith("Category:", $this->title)){
   return str_replace("Category:", "", $this->title);
  }
  else if(startsWith("101implementation:", $this->title)){
    return str_replace("101implementation:", "", $this->title);
  }
  else if(startsWith("Technology:", $this->title)){
    return str_replace("Technology:", "", $this->title);
  }
  else if(startsWith("Language:", $this->title)){
    return str_replace("Language:", "", $this->title);
  }
  else if(startsWith("101feature:", $this->title)){
   return str_replace("101feature:", "", $this->title);
  }
  else if(startsWith("101contributor:", $this->title)){
   return str_replace("101contributor:","", $this->title);
  }

  return $this->title;
 }

 function getFullTitle(){
  return $this->title;
 }
 
 function getFileName(){
  $t = $this->getTitle();
  $symbols = array(" ", "/");
  return str_replace($symbols, "_", $t);
 }
 
 function toTexMacro(){
    if (startsWith("Technology", $this->title)) {
      $tex = "\\newcommand{\\". getTexCommandName(str_replace('_','',$this->getTitle())) . "PageTitle}{\wikittref{". str_replace('_',' ',$this->getTitle()) ."}}" . PHP_EOL;
    }
    else
      $tex = "\\newcommand{\\". getTexCommandName(str_replace('_','',$this->getTitle())) . "PageTitle}{\wikiuqref{". str_replace('_',' ',$this->getTitle()) ."}}" . PHP_EOL;
    $tex .= "\\newcommand{\\". getTexCommandName(str_replace('_','',$this->getTitle())) . "PageIntent}{". ucfirst(formatter::toTex($this->intent)) ."}" . PHP_EOL;
    $tex .= "\\newcommand{\\". getTexCommandName(str_replace('_','',$this->getTitle())) . "PageDiscussion}{". formatter::toTex($this->discussion) ."}" . PHP_EOL;
	$tex .= "\\newcommand{\\". getTexCommandName(str_replace('_','',$this->getTitle())) . "PageDescription}{". formatter::toTex($this->description) ."}" . PHP_EOL;
	$tex .= "\\newcommand{\\". getTexCommandName(str_replace('_','',$this->getTitle())) . "PageTechnologies}{". formatter::toTex($this->technologies) ."}" . PHP_EOL;
    $tex = formatter::sourceLinks($this->getTitle(),$tex);
    return $tex;
 }
 
 function toTex(){
  $tex = "wikisite\\" . "category" . "{" . $this->getTitle() . "}{" . escape($this->intent) . "}";
  
  return $tex;
 }
 
 function __construct($title){
  $this->title = $title;
  $this->namespace = "";
  $this->sections = array();
  $this->rawDump = array();
  $this->content = getPageContent($title);
  if ($this->content == NULL)
   return false;
  $this->lastrev = getRivison($title,'older');
  $this->creation = getRivison($title,'newer');
  $this->getSections();
  $this->bibs = extractBibs($this->content);
  $this->intent = extractIntent($this->content);
  $this->discussion = extractContent($this->content, "==Discussion==");
  $this->description = extractContent($this->content, "==Description==");
  $this->technologies = extractContent($this->content, "==Technologies==");
  $this->objective = extractContent($this->objective, "==Objective==");
 }

  function getSections(){
   $pattern =  '/\s?\={2,3}\s*([A-Za-z\s]+)\s*\={2,3}/';
   preg_match_all($pattern, $this->content, $out, PREG_PATTERN_ORDER);
   foreach($out[1] as $section){
    if($section == '') continue;
    $section = trim($section);
    array_push($this->sections, $section);
    $this->rawDump[$section] = extractContent($this->content, "==". $section . "==");
   }
  return $rawDump;
   
  // $lastSectionIdx = count($out[1]);
  // $this->rawDump[$out[1][$lastSection]]
   
   //var_dump($rawDump);
 }

 function dumpToTex(){
  $tex = "";
  if($this->title == '') return '';
  if($this->title == NULL) return '';
  
  $tex = handleTitle($this->title);
  foreach($this->rawDump as $section=>$content){
   $title = str_replace(":", "", $this->title);
   $t = str_replace(" ", "", $title . $section) . "}";
   
   $tex .= "\\newcommand{\\" . getTexCommandName(str_replace("101", "", $t)) . "{" . formatter::toTex($content) ."}" . PHP_EOL; 
  }
  //var_dump($tex);
  return $tex;  
 }
}

function handleTitle($fullTitle){
  $out = explode(":", $fullTitle); 
  $namespace = "";
  $title = "";
  
  //page name can be either namespace:title or just title
  if(count($out) == 2){
   $namespace = $out[0];
   $title = $out[1];
  }
  else{
   $title = $fullTitle;
   $namespace = "";
  }
  $res = "\\newcommand{\\" . getTexCommandName(str_replace("101", "",($namespace . $title))). "Title}{\\wikiref{" . handleWikiRef($fullTitle) . "}{" . formatter::toTex($title) . "}}" . PHP_EOL;  
  return $res;
}

class CategoryPage extends Page{
 public $members;
  
 function __construct($title){
  parent::__construct($title);
  $this->namespace = "Category";
  $this->members = array();
  ECHO "Getting category members for " . $title . PHP_EOL;
  $subCats = getWpapi()->categorymembers($title);
  var_dump($subCats);

  if($subCats == NULL) return;
   foreach($subCats as $sc){
    if(substr_count($sc['title'],"Category") == 1){ //found a Category
	  ECHO "Adding a category page: " . $sc['title'] . PHP_EOL;
      $page = new CategoryPage($sc['title']);
      array_push($this->members, $page);
    }
    else if(substr_count($sc['title'],"101implementation") == 1){ //found an implementation page
	  ECHO "Adding an implementation page: " . $sc['title'] . PHP_EOL;
      $page = new ImplementationPage($sc['title']);
      array_push($this->members, $page);
    }
    else if(substr_count($sc['title'], "101feature") == 1){
	 ECHO "Adding an feature page: " . $sc['title'] . PHP_EOL;
     $page = new FeaturePage($sc['title']);
     array_push($this->members, $page);
    }
    else{
	ECHO "Adding a page: " . $sc['title'] . PHP_EOL;
    $page = new Page($sc['title']);
    array_push($this->members, $page);
   }
  } 
 }
 
 function getFullCategoryTree(){
  $memberTree = array();
  foreach($this->members as $m){
   if($m->namespace == "Category"){
    array_push($memberTree, $m);
    $childlen = $m->getFullCategoryTree();
    foreach($childlen as $c){
     array_push($memberTree, $c);
    }
   }   
  }
  
  return $memberTree;
 }
 
 function getImplementations(){
  $memberTree = array();
  foreach($this->members as $m){ //since we don't have nested implementations, top-level loop is OK
   if($m->namespace == "101implementation"){
    array_push($memberTree, $m);
   }   
  }
  
  return $memberTree;
 }
 
 
 private function getObjType($cat){
  if($cat->namespace == "Category"){
   return "concept";
  }
  
  return "instance";
 }
 

 private function getIntetByLevel($level){
  $default = "\\tab";
  for($i = 0; $i <= $level - 1; $i++){
    $default .= "\\tab";
  }
  return $default;
 }
 
 private function writeWithIdent($cat, $level){
   $tex .= $this->getIntetByLevel($level) . "\\" . $this->getObjType($cat) ."{" . formatter::handleLinks($cat->getFullTitle()) . "}{". ($cat->intent) . "}\n";
   //"\\" . $this->getObjType($cat) . "{\\wikiref{" . $cat->getFullTitle() . "}{".handleUmlauts($cat->getTitle()) ."}}{". formatter::toTex($cat->intent) . "}\n";
   foreach($cat->members as $c){
    $tex .= $this->writeWithIdent($c, $level + 1); 
   }
   
   return $tex;
 }

 private function writeWithIdentCategoriesOnly($cat, $level){
   $tex .= $this->getIntetByLevel($level) . "\\" . $this->getObjType($cat) ."{" . formatter::handleLinks($cat->getFullTitle()) . "}{". ($cat->intent) . "}\n";
   foreach($cat->members as $c){
	if($c->namespace == "Category") { 
		//ECHO "writeWithIdentCategoriesOnly" . PHP_EOL;
		//var_dump($c);
		$tex .= $this->writeWithIdentCategoriesOnly($c, $level + 1); }
   }
   
   return $tex;
 }
 
 function getDeepTex(){
  if ($this->content == NULL) return "";
  $tex = "\\tree{" . $this->getTitle() . "}{" . formatter::toTex($this->intent) . "}{\n" ;
  $level = 0;
  foreach($this->members as $m){
   $tex .= $this->writeWithIdent($m, $level);
  }
  $tex .= "}";  
  return $tex;
 }

 function getShallowTex(){
   if ($this->content == NULL)	return "";
   $tex = "\\tree{" . $this->getTitle() . "}{" . formatter::toTex($this->intent) . "}{\n" ;
   foreach($this->members as $m){
     $tex .= "\\tab\\" . $this->getObjType($m) . "{" . formatter::handleLinks($m->getFullTitle()) . "}{".  ($m->intent) . "}\n";
     //"{\\wikiref{" . $m->getFullTitle() . "}{".handleUmlauts($m->getTitle()) ."}}{". formatter::toTex($m->intent) . "}\n";
   }
   $tex .= "}";
   
   return $tex;
 }


function getClassifyTex(){
  if ($this->content == NULL) return "";
  $tex = "\\tree{" . $this->getTitle() . "}{" . formatter::toTex($this->intent) . "}{\n" ;
  $level = 0;
  foreach($this->members as $m){
   if($m->namespace == "Category")	{ $tex .= $this->writeWithIdentCategoriesOnly($m, $level); }
  }
  $tex .= "}";  
  return $tex;
 }

 function toTexMacro(){
 	if ($this->content == NULL)
   		return "";
    $tex = "\\newcommand{\\". getTexCommandName($this->getTitle()) . "CategoryTitle}{". $this->getTitle() ."}" . PHP_EOL;
    $tex .= "\\newcommand{\\". getTexCommandName($this->getTitle()) . "CategoryIntent}{". formatter::toTex($this->intent) ."}" . PHP_EOL;
    $tex .= "\\newcommand{\\". getTexCommandName($this->getTitle()) . "CategoryDescription}{". formatter::toTex($this->description) ."}" . PHP_EOL;
    return $tex;
 }
 
 function dumpToTex(){
   if ($this->content == NULL)
   	return "";
  return parent::dumpToTex();
 }
}


class ImplementationPage extends Page{
 public $languages;
 public $technologies;
 public $features;
 public $motivation;
 public $architecture;
 public $usage;
 public $contributors;
 public $spaces;
 public $illustration;
 public $issues;
  
 function getFeats(){
  return $this->features;
 } 
 
 function getTechs(){
   $techs = array();
   $pattern = "/(Technology:)([\w\W\s][^\]]+)(\]{2})/";
   foreach(preg_split( '/\r\n|\r|\n/', $this->technologies) as $line){
    if($line == '') continue;
    
    preg_match_all($pattern, $line, $out, PREG_PATTERN_ORDER);
     if($out[2][0] != ''){
       array_push($techs,trim(until("|",$out[2][0]))); 
     }
  }
  return $techs;
 }
 
 function getLangs(){
   $langs = array();
   $pattern = "/(Language:)([\w\W\s][^\]]+)(\]{2})/";
   foreach(preg_split( '/\r\n|\r|\n/', $this->languages) as $line){
    if($line == '') continue;
    
    preg_match_all($pattern, $line, $out, PREG_PATTERN_ORDER);  
     if($out[2][0] != ''){
       array_push($langs,trim(until("|",$out[2][0]))); 
     }
  }
  return $langs;
 } 
  
 function toTexMacro(){
   $tex = "\\newcommand{\\". getTexCommandName($this->getTitle()) . "ImplementationTitle}{\\wikiiref{". $this->getTitle() ."}}" . PHP_EOL; 
   $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "ImplementationIntent}{" . ucfirst(formatter::toTex($this->intent)) . "}" . PHP_EOL;
   $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "ImplementationMotivation}{" . formatter::toTex($this->motivation) . "}" . PHP_EOL;
   $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "ImplementationLanguages}{" . formatter::toTex($this->languages) . "}" . PHP_EOL;
   $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "ImplementationTechnologies}{" . formatter::toTex($this->technologies) . "}" . PHP_EOL;
   $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "ImplementationIllustration}{" . formatter::toTex($this->illustration) . "}" . PHP_EOL;
   $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "ImplementationArchitecture}{" . formatter::toTex($this->architecture) . "}" . PHP_EOL;
   $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "ImplementationUsage}{" . formatter::toTex($this->usage) . "}" . PHP_EOL;
   $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "ImplementationIssues}{" . formatter::toTex($this->issues) . "}" . PHP_EOL;
   
   $ftxt = "";
   foreach($this->features as $f)
   {
    $ftxt .= "* [[101feature:" . $f . "]]". PHP_EOL;
   }
  
      
   $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "ImplementationFeatures}{" . formatter::toTex(formatter::nestedList($ftxt)) . "}" . PHP_EOL;  
   $tex = formatter::sourceLinks($this->getTitle(),$tex);
   return $tex;
 } 

 function __construct($title){
  parent::__construct($title);
  $this->namespace = "101implementation";
  
  $this->languages = extractContent($this->content, "==Languages=="); 
  $this->technologies = extractContent($this->content, "==Technologies==");  
  $featuresContent = extractContent($this->content, "==Features==");
  $this->features = array();
  $pattern = "/(101feature:)([\w\W\s][^\]]+)(\]{2})/"; 
  foreach(preg_split( '/\r\n|\r|\n/', $featuresContent) as $line){
    if($line == '') continue;
    
    preg_match_all($pattern, $line, $out, PREG_PATTERN_ORDER);
     if($out[2][0] != ''){
       array_push($this->features,$out[2][0]); //$feature);
     }
  }
  
  $this->spaces = array();
  foreach(preg_split( '/\r\n|\r|\n/', $this->technologies) as $t){
   if($t == '') continue;
   $pattern =  "/(Technology:[\w\W\s][^\]]+)(\]{2})/";
   preg_match_all($pattern, $t, $out, PREG_PATTERN_ORDER);
   
   if($out[1][0] == '') continue;

   $tp = new TechnologyPage($out[1][0]);
   foreach($tp->spaces as $s){
    array_push($this->spaces, $s);
   }
  }  
    
  $this->motivation = extractContent($this->content, "==Motivation==");
  $this->architecture = extractContent($this->content, "==Architecture==");
  $this->usage = extractContent($this->content, "==Usage==");
  $this->contributors = extractContent($this->content, "==Contributors==");
  $this->illustration = extractContent($this->content, "==Illustration==");
  $this->issues = extractContent($this->content, "==Issues==");
 }
}

class LanguagePage extends Page{
 public $description;
 function __construct($content){
 parent::__construct($content);
 $this->description = extractContent($this->content, "==Description==");
 $this->namespace = "Language";
 }
 
  function toTexMacro(){
   $tex = "\\newcommand{\\". getTexCommandName($this->getTitle()) . "LanguageTitle}{". $this->getTitle() ."}" . PHP_EOL;
   $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "LanguageIntent}{" . formatter::toTex($this->intent) . "}" . PHP_EOL;
   $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "LanguageDescription}{" . formatter::toTex($this->description) . "}" . PHP_EOL;
   return $tex;
  }

}

class TechnologyPage extends Page{
 public $description;
 public $spaces;
 function __construct($title){
  parent::__construct($title);
  $this->description = extractContent($this->content, "==Description==");
  $this->namespace = "Technology";
  
  $spacesContent = extractContent($this->content, "==Spaces==");  
  $this->spaces = array();
  $pattern = "/(\*(\s)*\[{2})([\w\W\s][^\]]+)(\]{2})/";
  foreach(preg_split( '/\r\n|\r|\n/', $spacesContent) as $line){
   if($line == '') continue;

   preg_match_all($pattern, $line, $out, PREG_PATTERN_ORDER);
   if($out[3][0] != ''){
    array_push($this->spaces, $out[3][0]);
   }
  } 
 }
 
 function toTexMacro(){
   $tex = "\\newcommand{\\". getTexCommandName($this->getTitle()) . "TechnologyTitle}{". formatter::toTex(trim($this->getTitle())) ."}" . PHP_EOL;
   $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "TechnologyIntent}{" . formatter::toTex(trim($this->intent)) . "}" . PHP_EOL;
   $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "TechnologyDescription}{" . formatter::toTex(trim($this->description)) . "}" . PHP_EOL;
   return $tex;
  }
}
   
class FeaturePage extends Page{
 public $description;
 public $illustration;
 function __construct($title){
  parent::__construct($title);
  $this->description = extractContent($this->content, "==Description==");
  $this->illustration = extractContent($this->content, "==Illustration==");
  $this->namespace = "101feature";
 }
 
 function toTexMacro(){
  $tex = "\\newcommand{\\". getTexCommandName($this->getTitle()) . "FeatureTitle}{". $this->getTitle() ."}" . PHP_EOL;
  $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "FeatureIntent}{" . formatter::toTex($this->intent) . "}" . PHP_EOL;
  $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "FeatureDescription}{" . formatter::toTex($this->description) . "}" . PHP_EOL;
  $tex .= "\\newcommand{\\" . getTexCommandName($this->getTitle()) . "FeatureIllustration}{" . formatter::toTex($this->illustration) . "}" . PHP_EOL;
  return $tex;
 }
}
class Feature{
 public $name;
 function __construct($content){
  $this->name = $content;
 }
}




