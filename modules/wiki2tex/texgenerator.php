<?php

define('BASE_PATH',str_replace('wiki2tex','',dirname(__FILE__)));
error_reporting(E_ALL);
ini_set('display_errors','On');
 
$outputShallowFolder = BASE_PATH . "wiki2tex/tex/ontology/data/shallow/";
$outputDeepFolder = BASE_PATH . "wiki2tex/tex/ontology/data/deep/";
$outputClassificationFolder = BASE_PATH . "wiki2tex/tex/ontology/data/classification/";
$dataFolder = BASE_PATH . "wiki2tex/tex/ontology/data/";

$texFolder = BASE_PATH . "wiki2tex/tex/content/data/";
$texFolderMatrix = BASE_PATH . "wiki2tex/tex/matrix/data/";
$texFolderDump = BASE_PATH . "wiki2tex/tex/dump/data/";

$filesFolder = BASE_PATH . "wiki2tex/tex/files/";

$implsFolder = BASE_PATH. "wiki2tex/tex/impl/data/";
$ttcsFolder = BASE_PATH. "wiki2tex/tex/ttc/data/";

require_once(BASE_PATH . '../libraries/MediaWikiAPI/ApiWrapper2.php');
require_once(BASE_PATH . '../libraries/MediaWikiAPI/Utils.php');
require_once("commandLine.php");
require_once("formatter.php");

function getIntetByLevel($level){
  $default = "\\tab";
  for($i = 0; $i <= $level - 1; $i++){
    $default .= "\\tab";
  }
  return $default . "\\tab";
}


function escape($txt){
  $escaped = str_replace("#", "\#", $txt);
  $escaped = str_replace('$', "\$", $escaped);
  //$escaped = str_replace('<', "\<", $escaped);
  //$escaped = str_replace('<', "\<", $escaped);
  $escaped = str_replace("_", "\_", $escaped);
  return $escaped;
}

class OntyGenerator{
  private $catPage;
  
 function __construct($catPage){
    $this->catPage = $catPage;
  }
  
 function generateCategoryFile(){
  $categoryFile = "";
  $allCategories = $this->catPage->getFullCategoryTree();
  foreach($allCategories as $cat){
     $symbols = array(" ", "/");
     $fileName = str_replace($symbols, "_", $cat->getTitle());     
     $categoryFile .= "\categoryfile{" . $fileName ."}" . PHP_EOL;
  }
 
  return $categoryFile;
 }

function generateCategoryOnlyFile(){
  $categoryFile = "";
  $allCategories = $this->catPage->getFullCategoryTree();
  foreach($allCategories as $cat){
	if($cat->namespace == "Category"){
     $symbols = array(" ", "/");
     $fileName = str_replace($symbols, "_", $cat->getTitle());     
     $categoryFile .= "\categoryfile{" . $fileName ."}" . PHP_EOL;
   }
  }

  return $categoryFile;
 }


 
 function generateShallowTexStructure($catPage){
   $shallowTex = "\\tree{" . $catPage->getTitle() . "}{" . escape($catPage->intent) . "}{\n" ;
   foreach($catPage->members as $m){
     $shallowTex .= "\\tab\concept{" . $m->getTitle() . "}{". escape($m->intent) . "}\n";
   }
   
   return $shallowTex;
 }
}                                                                                      

$args = CommandLine::parseArgs($_SERVER['argv']);

//$args['mode'] = 'matrixif';
//$args['ilist'] = "../lists/pppjImpls.lst";
//$args['output'] = "pppjif";


if($args['mode'] == 'singlePage'){
  $title = $args['title'];
  if (startsWith("101implementation:",$title)) {
    echo $title;
    $page = new ImplementationPage($title);
    #var_dump($page);
    #echo $page->dumpToTex();
    var_dump(formatter::toTex($page->illustration));
  }


}
else if($args['mode'] == 'dump'){
   echo "Entering dump mode, please wait..." . PHP_EOL;
   $wiki = new Wiki();
   print($texFolderDump . PHP_EOL);
   $f = fopen($texFolderDump . "macros.tex", "w+");
   $allPages = $wiki->getAllPages();
   //echo "DUMP: " . PHP_EOL;
   //var_dump($allPages);
   echo "Getting categories pages";
   $catPages = $wiki->getCategoryPages();
   echo "Dumping wiki content..." . PHP_EOL;
   $pages = array();
   $pages = array_merge($catPages, $allPages);
   $pages = $allPages;
   
   $content = "";
   $i = 0;
   foreach($pages as $page){
	  ECHO $page->getTitle() . PHP_EOL;
    $tex = $page->dumpToTex();
    if(strstr($tex, "CategorymetaTitle") == FALSE){
      var_dump($tex);
      $content .= $tex;
    }
   }
   foreach($catPages as $page){
	  ECHO $page->getTitle() . PHP_EOL;
    $tex = $page->dumpToTex();
    if(strstr($tex, "CategorymetaTitle") == FALSE){
      $content .= $tex;
    }
   }
   fwrite($f, $content);
   fclose($f);
}
else if($args['mode'] == 'ontology'){ //generate ontology
  echo "entering ontology generation mode, please wait...";
  $tex = "";
  $wiki = new Wiki();
  $base = new CategoryPage("Base");
  $generator = new OntyGenerator($base);
  $categoryFile = $generator->generateCategoryFile();
  //$f = fopen($dataFolder . "files.tex", 'w+') or die("can't open file");
  //fwrite($f, $categoryFile);
  //fclose($f);
	
  $categoryFile = $generator->generateCategoryOnlyFile();
  $f = fopen($dataFolder . "filesCategory.tex", 'w+') or die("can't open file");
  fwrite($f, $categoryFile);
  fclose($f);

  echo PHP_EOL . "generating shallow ontology";
  $allCategories = $base->getFullCategoryTree();
  
  foreach($allCategories as $cat){
   $fileName = $cat->getFileName() . ".tex";
   $tex = $cat->getShallowTex();
   $f = fopen($outputShallowFolder . $fileName, 'w+') or die("can't open file");	
   //$text = formatter::toTex($tex);
   //fwrite($f, $text . PHP_EOL);
   foreach (explode(PHP_EOL, $tex) as $line)
   {
    $line = formatter::toTex($line);
    fwrite($f, $line . PHP_EOL);
   } 
   fclose($f);
  }
  
  echo PHP_EOL . "generating deep ontology";
  foreach($allCategories as $cat){
   $tex = $cat->getDeepTex();
   $fileName = $cat->getFileName() . ".tex";
   $f = fopen($outputDeepFolder . $fileName, 'w+') or die("can't open file");
   foreach (explode(PHP_EOL, $tex) as $line)
   {
     $line = formatter::toTex($line);
     fwrite($f, $line . PHP_EOL);
    }
   fclose($f);
  }

  echo PHP_EOL . "generating classification ontology";
  foreach($allCategories as $cat){
       $tex = $cat->getClassifyTex();
	   $fileName = $cat->getFileName() . ".tex";
	   $f = fopen($outputClassificationFolder . $fileName, 'w+') or die("can't open file");
	   foreach (explode(PHP_EOL, $tex) as $line)
	   {
	     $line = formatter::toTex($line);
	     fwrite($f, $line . PHP_EOL);
	   }
   fclose($f);
  }
  
}
else if ($args['mode'] == 'implContents') {
  $titles = explode(',',$args['titles']);
  $note = explode('%', $args['node']);
  $nTitle = $note[0];
  $nNote = str_replace('L"a','L\\"a',str_replace('_',' ',$note[1]));
  echo $nNode;
  $otherTitles = explode(',', $args['otitles']);
  $macroTex = '';
  $implsTex = '';
  $fMacro = fopen($implsFolder.'macros.tex', 'w+');
  $fBib = fopen($implsFolder.'impls.bib', 'w+');
  $fImpls = fopen($implsFolder.'implementations.tex', 'w+');
  $bibs = array();
  foreach($titles as $title){
    $pureTitle = str_replace('101implementation:','',$title); 
    $ucTitle = ucfirst($pureTitle);
    $implTexTit = 'impls/impl'.str_replace('5','Five',$ucTitle).'.tex';
    
    // adding to mactro
    $macroTex .= '\\input{../../../101dev/tools/texgenerator/tex/impl/data/'.$implTexTit.'}'.PHP_EOL;
    $s = new ImplementationPage($title);
    // adding to implementations.tex
    if ($title != $nTitle){
      if ($s->issues != ''){
        $implsTex .= '\\iuwiki{'.str_replace('5','Five',$pureTitle).'}\\newpage'.PHP_EOL;
      } else {
        $implsTex .= '\\iwiki{'.str_replace('5','Five',$pureTitle).'}\\newpage'.PHP_EOL;
      }
    } else {
      $implsTex .= '\\inwiki{'.str_replace('5','Five',$pureTitle).'}\\newpage'.PHP_EOL;
    }
    
    
    // creating tex file for implementation
    $fImplMacro = fopen($implsFolder.$implTexTit,'w+');
    
    
    echo 'Saving macro for "'.$title.'"... ';
    
    $implMacroTex = $s->toTexMacro();
    if ($title == $nTitle){
    $implMacroTex .= "\\newcommand{\\". str_replace('_','', str_replace(' ','',str_replace('5','Five',$s->getTitle()))) . "ImplNote}{".$nNote."}".PHP_EOL;
    } 
    $implMacroTex = formatter::intLinks($implMacroTex, array_merge($titles,$otherTitles));
    $implMacroTex .= "\\newcommand{\\". str_replace('_','', str_replace(' ','',str_replace('5','Five',$s->getTitle()))) . "ImplLabel}{". str_replace('_','', str_replace(' ','',$s->getTitle())) ."}" . PHP_EOL;
    fwrite($fImplMacro,$implMacroTex);
    fclose($fImplMacro);
    echo 'DONE'.PHP_EOL;
    echo 'Getting BibTex... ';
    foreach($s->bibs as $bib){
      array_push($bibs,$bib);
    }
    echo 'DONE'.PHP_EOL.PHP_EOL;
  }
  echo 'Saving collective macro file "macros.tex"... ';
  fwrite($fMacro, $macroTex);
  fclose($fMacro);
  echo 'DONE'.PHP_EOL;
  echo 'Saving "implementations.tex"... ';
  fwrite($fImpls, $implsTex);
  fclose($fImpls);
  echo 'DONE'.PHP_EOL;
  echo 'Saving .bib for implementations... ';
  fwrite($fBib,implode(PHP_EOL,$bibs));
  fclose($fBib);
  echo 'DONE'.PHP_EOL;
  
}
else if ($args['mode'] == 'ttcContents') {
  $titles = explode(',',$args['titles']);
  $macroTex = '';
  $ttcsTex = '';
  //var_dump($linkRefs);
  $fMacro = fopen($ttcsFolder.'macros.tex', 'w+');
  $fBib = fopen($ttcsFolder.'ttcs.bib', 'w+');
  $fTtcs = fopen($ttcsFolder.'ttcs.tex', 'w+');
  $bibs = array();
  $allLinks = array();
  foreach ($titles as $title) {
    $pureTitle = str_replace('_','',str_replace('Category:','',str_replace('Technology:','',$title)));
    $ucTitle = ucfirst($pureTitle);
    $ttcTexTit = 'ttcs/ttc'.$ucTitle.'.tex'; 
    
    // adding to mactro
    $macroTex .= '\\input{../../../101dev/tools/texgenerator/tex/ttc/data/'.$ttcTexTit.'}'.PHP_EOL;
    
    $s = new Page($title);
     // adding to ttcs.tex
    if ($s->discussion != '') {
      $ttcsTex .= '\\ttcdwiki{'.$pureTitle.'}'.PHP_EOL;
    } else {
	  if ($s->technologies != '') {
	    $ttcsTex .= '\\ttcdtwiki{'.$pureTitle.'}'.PHP_EOL;
	  } else {
	    $ttcsTex .= '\\ttcwiki{'.$pureTitle.'}'.PHP_EOL;
	  }
    }
    
    
    
    $fTtcMacro = fopen($ttcsFolder.$ttcTexTit,'w+');
    echo 'Saving macro for "'.$title.'"... ';
    
    $ttcMacroTex = $s->toTexMacro();
    $ttcMacroTex = formatter::intLinks($ttcMacroTex,$titles);
    $ttcMacroTex .= "\\newcommand{\\". str_replace('_','', str_replace(' ','',$s->getTitle())) . "TtcLabel}{". str_replace('_','', str_replace(' ','',$s->getTitle())) ."}" . PHP_EOL;
    //var_dump($links);
    fwrite($fTtcMacro, $ttcMacroTex);
    fclose($fTtcMacro);
    echo 'DONE'.PHP_EOL;
    echo 'Getting BibTex... ';
    foreach($s->bibs as $bib){
      $newbib = '';
      $i = 0;
      foreach(preg_split( '/\r\n|\r|\n/', $bib) as $bibline) {
        if ($i != 0 && startsWith('title',ltrim($bibline))) {
          $bibline = preg_replace('/([A-Z]+)/','{\1}',$bibline);
        }
        $newbib .= $bibline.PHP_EOL;
        $i += 1;
        
      }
      array_push($bibs,$newbib);
    }
    echo 'DONE'.PHP_EOL.PHP_EOL; 
  }
  echo 'Saving collective macro file "macros.tex"... ';
  fwrite($fMacro, $macroTex);
  fclose($fMacro);
  echo 'DONE'.PHP_EOL;
  echo 'Saving "ttcs.tex"... ';
  fwrite($fTtcs, $ttcsTex);
  fclose($fTtcs);
  echo 'DONE'.PHP_EOL;
  echo 'Saving .bib for ttcs... ';
  fwrite($fBib,implode(PHP_EOL,$bibs));
  fclose($fBib);
  echo 'DONE'.PHP_EOL;
}


else if($args['mode'] == 'content'){ //generate tex wiki pages representation
  $wiki = new Wiki();
 
  $fMacro = fopen($texFolder . "macros.tex", "w+"); 
	
  $baseCat = new CategoryPage("Category:Base");
  fwrite($fMacro, $baseCat->toTexMacro());

 
  ECHO "Getting categories".PHP_EOL;
  $catPages = $wiki->getCategoryPages();
  var_dump($catPages);
  
  ECHO "Getting 101implementation category" . PHP_EOL;
  $catImpl = new CategoryPage("101implementation");
  ECHO "Getting all implementation pages" . PHP_EOL;
  $impl = $catImpl->getImplementations();
  
  ECHO "Getting all language pages" . PHP_EOL;
  $allLangs = $wiki->getLanguagepages();

  ECHO "Getting all technologies pages" . PHP_EOL;
  $allTechnologies = $wiki->getTechnologyPages();
  //echo "Number of technology pages"; 
  // echo sizeof($allTechnologies) ;
  $catFeature = new CategoryPage("101feature");
  
  ECHO "Getting all other pages" . PHP_EOL;
  $allPages = $wiki->getAllPages();  
 
  $fImpl = fopen($texFolder . 'implementations.tex', 'w+');
  foreach($impl as $i){
    fwrite($fImpl, "\\iwiki{" . getTexCommandName($i->getTitle()) . "}" . PHP_EOL);
    // echo PHP_EOL . $i->getTitle() . PHP_EOL;
    //var_dump($i->toTexMacro());
    fwrite($fMacro, $i->toTexMacro());
  }
  foreach($allLangs as $lang){
   //var_dump($lang->toTexMacro()); 
   fwrite($fMacro, $lang->toTexMacro());
  }
  ECHO "Dumping technologies" . PHP_EOL;
  foreach($allTechnologies as $tech){
    $tex = $tech->toTexMacro();
    fwrite($fMacro, $tex);
  }
  $categories = array();  
  $cat = array();
  
  ECHO "Dumping Features" . PHP_EOL;
  foreach($catFeature->members as $cf){
    //array_push($categories, $cf->getTitle());
    fwrite($fMacro, "\\newcommand{\\" .getTexCommandName($cf->getTitle()) . "FeatureCategory}{" . $cf->getTitle() ."}". PHP_EOL);
	foreach($cf->members as $f){
	  if(in_array($f->getFullTitle(), $cat) == FALSE){
		ECHO $f->getFullTitle() . PHP_EOL;
	    fwrite($fMacro, $f->toTexMacro());
	    array_push($cat, $f->getFullTitle());
	    if($f->namespace == "Category"){
		 foreach($f->members as $fm){
			ECHO $fm->getFullTitle() . PHP_EOL;		
			fwrite($fMacro, $fm->toTexMacro());
		    array_push($cat, $fm->getFullTitle());
	     }
	    }
	   }
    }
  }
  
  ECHO "Dumping other pages" . PHP_EOL;
  foreach($allPages as $p){
    if(strstr($p->getFullTitle(), ":") == FALSE){
	 //ECHO $p->getFullTitle() . PHP_EOL;
     fwrite($fMacro, $p->toTexMacro());
    }
  }
  
  echo "Full base category tree" . PHP_EOL;
  foreach($baseCat->getFullCategoryTree() as $c){
    if($c->namespace == "Category"){
      if((in_array($c->getTitle(), $categories) == FALSE) && (in_array($c->getFullTitle(), $cat) == FALSE)) { //!!!  
	   //ECHO $c->getFullTitle() . PHP_EOL;	
       fwrite($fMacro, $c->toTexMacro());
       array_push($categories, $c->getTitle());
      }
    }
  }
 
  fclose($fImpl);
  fclose($fMacro);

  $fLang = fopen($texFolder . "languages.tex", "w+");
  foreach($allLangs as $lang){
    fwrite($fLang, "\\lwiki{" . getTexCommandName($lang->getTitle()) . "}". PHP_EOL);
  }
  fclose($fLang);

  $fTech = fopen($texFolder . "technologies.tex", "w+");
  foreach($allTechnologies as $t){
    fwrite($fTech, "\\twiki{" .getTexCommandName($t->getTitle()) . "}" . PHP_EOL);
  }
  fclose($fTech);
  
  $fFeatures = fopen($texFolder . "features.tex", "w+");
  foreach($catFeature->members as $cf){
	echo $cf->getTitle() . " : " . $cf->namespace . PHP_EOL;
    fwrite($fFeatures, "\\fcwiki{" .getTexCommandName($cf->getTitle()) . "}" . PHP_EOL);
    foreach($cf->members as $f){
	  echo "  " . $f->getTitle() . " : " . $f->namespace . PHP_EOL;
	  if(count($f->members) > 0){
		//fwrite($fFeatures, "\\fcwiki{" .getTexCommandName($f->getTitle()) . "}" . PHP_EOL);
		foreach($f->members as $fm){
		 echo "  " . $fm->getTitle() . " : " . $f->namespace . PHP_EOL;	 
	     fwrite($fFeatures, "\\fwiki{" .getTexCommandName($fm->getTitle()) . "}" . PHP_EOL);		 
		}
	  }
      else fwrite($fFeatures, "\\fwiki{" .getTexCommandName($f->getTitle()) . "}" . PHP_EOL);
    }    
  }
  fclose($fFeatures);
  
  $fCategories = fopen($texFolder . "categories.tex", "w+");
  fwrite($fCategories, "\\cwiki{" . getTexCommandName($baseCat->getTitle()) . "}" . PHP_EOL);
  foreach($baseCat->getFullCategoryTree() as $c){
    if($c->namespace == "Category"){
      fwrite($fCategories, "\\cwiki{" . getTexCommandName($c->getTitle()) . "}" . PHP_EOL);
    }
  }  
  fclose($fCategories);
  
    
  $fPages = fopen($texFolder . "pages.tex", "w+");
  foreach($allPages as $p){
    if(strstr($p->getFullTitle(), ":") == FALSE){
      fwrite($fPages,  "\\pwiki{" . getTexCommandName($p->getTitle()) . "}" . PHP_EOL);
    }
  }
  fclose($fPages);
 

  //formatTex();
}
else if(($args['mode'] == 'matrixif') || ($args['mode'] == 'matrixis') || ($args['mode'] == 'matrixts')){
  $output = ($texFolderMatrix . $args['mode'] . ".tex");
  if($args['output'] != ''){
    $output = $texFolderMatrix . $args['output'] . ".tex";
  }
  
  var_dump($output);
  
  $ilist = array();
  $tlist = array();
    
  if($args['ilist'] != ''){
    $ilist = file(realpath($args['ilist']), FILE_IGNORE_NEW_LINES|FILE_SKIP_EMPTY_LINES);
  }
  if($args['tlist'] != ''){
    $tlist = file(realpath($args['tlist']), FILE_IGNORE_NEW_LINES|FILE_SKIP_EMPTY_LINES);
  }
  
 $wiki = new Wiki();
 $features = $wiki->getFeaturePages();
 $catImpl = new CategoryPage("101implementation");
 $impl = $catImpl->getImplementations();
 $technologies = $wiki->getTechnologyPages();
 
 if($args['mode'] == 'matrixif'){
  buildImplementationFeaturesMatrix($impl, $features, $output, $ilist);
 }
 else if($args['mode'] == 'matrixis'){
   buildImplSpacesMatrix($impl, $ilist, $output);
 }
 else if($args['mode'] == 'matrixts'){
   buildTechnicalSpacesMatrix($technologies, $tlist, $output);
 }
}
else{
  die('the following params are supported: --mode=ontology|content|matrixif|matrixis|matrixts|singlePage' . PHP_EOL);
}

function getBy($catImpl, $val){
  $impl = $catImpl->getImplementations();
  foreach($impl as $i){
    if($i->getTitle() == $val) return $i;
  }
  
  return NULL;
}

function getTechologyBy($technologies, $val){
  foreach($technologies as $t){
    if($t->getTitle() == $val) return $t;
  }
}



function buildTableHeader($features, $delimPosition){
 $numCols = count($features);
  $th = "\\begin{tabular}{l";
 for($i=0; $i<$numCols; $i++){
  if(gettype($delimPosition) == 'array'){
    if(in_array($i, $delimPosition)){
      $th .= "||c";
    }
    else{
      $th .= "|c";
    } 
  }
  else{
    if($i != $delimPosition){
      $th .= "|c";
    }
    else{
      $th .= "||c";
    } 
  }
 } 
 $th .= "}" . PHP_EOL;
 foreach($features as $f){
  $th .= "& \\hLegend{" . $f . "} ";
 }
 return $th . PHP_EOL . "\\newRow" . PHP_EOL;
}


function buildTechnicalSpacesMatrix($technologies, $tlist, $output){
   $catSpace = new CategoryPage("Technical space");
   $spaces = $catSpace->members;
   
   $catSegments = new CategoryPage("Technical segment");
   $segments = $catSegments->members;
   
   $spaceNames = array();
   foreach($spaces as $s){
    array_push($spaceNames, $s->getTitle());
   }
   foreach($segments as $s){
    array_push($spaceNames, $s->getTitle());
  }  
   
   $implSpaces = array();
   foreach($spaceNames as $s){
    $implSpaces[$s] = 0;
   }
 
   $spaceFrequency = array();
   foreach($spaceFrequency as $sf){
    $spaceFrequency[$sf] = 0;  
   } 
 
 foreach($technologies as $t){
  foreach($spaceNames as $sn){
   if(in_array($sn, $t->spaces)){
    $implSpaces[$sn] ++;
    $spaceFrequency[$t->getTitle()] ++;
   }
  }
 }
 
 asort($implSpaces, SORT_NUMERIC);
 asort($spaceFrequency, SORT_NUMERIC);
 $implSpaces = array_reverse($implSpaces);
 $spaceFrequency = array_reverse($spaceFrequency);
 
 $content = buildTableHeader($spaceNames, count($spaces));//array_keys($implSpaces));
 
 if(count($tlist) > 0){
  $spaceFrequency = array_flip($tlist);
 }
 
 
 foreach($spaceFrequency as $sf=>$v){
  $t = getTechologyBy($technologies, $sf);
  
  $atleastOnce = false;
  foreach($spaceNames as $sn){
  //foreach(array_keys($implSpaces) as $sn){
   if(count($t->spaces) == 0) break; 
   if(in_array($sn, $t->spaces)){
    $atleastOnce = true;
   }
  }
  
  $technicalSegments = array();
  foreach($segments as $s){ 
    array_push($technicalSegments, $s->getTitle());
  }
  
  if($atleastOnce == true)
  {
    $row .= "\\vLegend{". $t->getTitle() ."}";
    foreach($spaceNames as $sn){
    //foreach(array_keys($implSpaces) as $sn){
    if(in_array($sn, $t->spaces)){
        $row .= " & \\okValue";
    }
    else{
     $row .= " & \\noValue";
    }
   } 
   $row .= PHP_EOL . "\\newRow" . PHP_EOL;    
  }
 }
 
 $content .= $row . "\\end{tabular}";
 
 global $texFolderMatrix;
 $f = fopen($output, "w+");
 fwrite($f, $content); 
 fclose($f);  
}

function buildImplSpacesMatrix($impl, $whiteList, $output){
  $catSpace = new CategoryPage("Technical space");
  $spaces = $catSpace->members;
  $arrSpaces = array();
  foreach($spaces as $s){
    array_push($arrSpaces, $s->getTitle());
  }
  
   $catSegments = new CategoryPage("Technical segment");
   $segments = $catSegments->members;

   foreach($segments as $s){
    array_push($arrSpaces, $s->getTitle());
  }  
  
  $content = buildTableHeader($arrSpaces, count($spaces));
  
  if(count($whiteList) > 0){
    $impl = array();
    foreach($whiteList as $wl){
      array_push($impl, new ImplementationPage("101implementation:" . $wl));
    }
  }
  
  foreach($impl as $i){
    $row .= "\\vLegend{". $i->getTitle() ."}";
    foreach($arrSpaces as $s){
      $sp = $i->spaces;
     if(in_array($s, $sp)){
      $row .= " & \\okValue";
     }
     else{
      $row .= " & \\noValue";
     }
    }
    $row .= PHP_EOL . "\\newRow" . PHP_EOL;
  }
  
  $content .= $row . "\\end{tabular}";
  global $texFolderMatrix;
  $f = fopen($output, "w+");
  fwrite($f, $content);
  fclose($f);
}

function buildImplementationFeaturesMatrix($impl, $features, $output, $ilist){
 $catImpl = new CategoryPage("101implementation");
 $featureNames = array();
 foreach($features as $f){
  array_push($featureNames, $f->getTitle());
 }
 $row = "";
 $implFeatures = array();
 foreach($featureNames as $fn){
  $implFeatures[$fn] = 0;
 }
 
 $featureFrequency = array();
 foreach($featureFrequency as $ff){
  $featureFrequency[$ff] = 0;  
 }
 foreach($impl as $i){
  if((count($ilist) > 0) && (in_array($i->getTitle(), $ilist) == false)) continue;
  
  foreach($featureNames as $fn){
   if(in_array($fn, $i->features)){
    $implFeatures[$fn] ++;
    $featureFrequency[$i->getTitle()] ++;
   }
  }
 }
 
 asort($implFejatures, SORT_NUMERIC);
 asort($featureFrequency, SORT_NUMERIC);
 $implFeatures = array_filter(array_reverse($implFeatures));
 $featureFrequency = array_reverse($featureFrequency);

 if(count($ilist) > 0){
  $featureFrequency = array_flip($ilist);
 }
 
 $implFeatures = array_keys($implFeatures);
 
 $featureNames = array();
 $delims = array();
 $cat = new CategoryPage("101basics");
 $i = 0;
 foreach($cat->members as $f){
  if(in_array($f->getTitle(), $implFeatures)){
     array_push($featureNames, $f->getTitle());
     $i++;
  } 
 }
 array_push($delims, $i);
 
 $cat = new CategoryPage("101capabilities");
 foreach($cat->members as $f){
  if(in_array($f->getTitle(), $implFeatures)){
     array_push($featureNames, $f->getTitle());
     $i++;
  } 
 }
 array_push($delims, $i);
 
 $cat = new CategoryPage("101extras");
 $i = 0;
 foreach($cat->members as $f){
  if(in_array($f->getTitle(), $implFeatures)){
     array_push($featureNames, $f->getTitle());
     $i++;
  } 
 }
 //array_push($delims, count($delims) + $i);
 
 $content = buildTableHeader($featureNames, $delims);
 
 foreach($featureFrequency as $ff=>$v){
 // if($v == 0) continue;
  $impl = getBy($catImpl, $ff);
  if($impl == NULL) {
    echo "Please check the consistency of the input whitelist. Implementation " . $ff . " has not beed found" . PHP_EOL;
    exit(1);
  }
  //apply whitelist
  if(count($ilist) > 0){
    if(in_array($impl->getTitle(), $ilist) == false){
      continue;
    }
  }
  $row .= "\\vLegend{". $impl->getTitle() ."}";
  foreach($featureNames as $fn){
  //foreach(array_keys($implFeatures) as $fn){
   if(in_array($fn, $impl->features)){
    $row .= " & \\okValue";
   }
   else{
    $row .= " & \\noValue";
   }
  }
  $row .= PHP_EOL . "\\newRow" . PHP_EOL;
 }
 
 $content .= $row . "\\end{tabular}";
  
 $f = fopen($output, "w+");
 fwrite($f, $content); 
 fclose($f);
}
echo PHP_EOL . "ALL DONE" . PHP_EOL;





