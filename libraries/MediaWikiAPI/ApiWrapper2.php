<?php

//define('BASE_PATH',str_replace('API','',dirname(__FILE__)));
require_once('ApiWrapper.php' );
require_once('Pages.php');

class Wiki{

    function getPage($title){
      $page = getPage();
      return $page;   
    }  
      
    function getAllPages(){
	    ECHO "Getting all pages" . PHP_EOL;
        $allPages = array();
        $pages = getAllPages();
        foreach($pages as $p){
            $page = new Page($content = $p['title']);
            echo $page->getFullTitle() . PHP_EOL;
            array_push($allPages, $page);
        }  
        $pages101 = get101companiesPages(); //!!
        foreach($pages101 as $p){
	     	$page = new Page($content = $p['title']);
            array_push($allPages, $page);
			ECHO "101companies page found: " .  $page->getFullTitle() . PHP_EOL;	
        } 
        return $allPages;
       // var_dump($allPages);
    }
    function getLanguagePages(){
      $res = array();
      $allLangs = getAllLanguages();
      // var_dump($allLangs);
      foreach($allLangs as $lang){
	$page = new LanguagePage($content = $lang['title']);
	array_push($res, $page);
	//$l = str_replace("Language:", '', $lang['title']);
        //array_push($res, str_replace(" ", "", $l));
      }

      return $res;
    }

    function getTechnologyPages(){
      $res = array();
      $allTechn = getAllTechnologies();
      foreach($allTechn as $t){
	$page = new TechnologyPage($content = $t['title']);
	//$l = str_replace("Technology:", '', $lang['title']);
	// array_push($res, str_replace(" ", "", $l));
	array_push($res, $page);
      }
      
      return $res;
     }
     
     function getCategoryPages(){
        $res = array();
        $categories = getWpapi()->listcategories();
       foreach($categories as $c){
         $page = new CategoryPage($content = "Category:" . $c['*']);
         array_push($res, $page);
        }
      return $res;
     }
     
    function getFeaturePages(){
     $res = array();
     $allFeatures = getWpapi()->listprefix("101feature:");
     var_dump($allFeatures); 
     foreach($allFeatures as $f){
      $page = new FeaturePage($content = $f['title']);
      array_push($res, $page);
     }
      return $res;
    }
}
