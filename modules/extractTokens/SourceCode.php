<?php defined('_MEGALIB') or die("No direct access") ;
require_once ABSPATH_SRC_GESHI_LIBRARY.'/geshi.php' ;


/**
* @param Any? $value a value or null
*/
function mixedValueSummary($value,$valueIfEmpty=null,$returnKind=false) {
  $valueToReturn = $value
    ? $value
    : (isset($valueIfEmpty)?$valueIfEmpty : $value) ;
  if (!$returnKind) {
    return $valueToReturn ;
  } else {
    $r = array() ;
    $r['kind']=typeOf($valueToReturn) ;
    $r['value']=$valueToReturn ;
    return $r ;
  }
}

/**
 * A GeSHI extension with introspection of language descriptions, metrics on such
 * language descriptions. In particular getLanguagePropertyHTMLMatrix provides a
 * comparative summary of all existing language descriptions.
 * 
 * Provides as well some helper function such as getLanguageFromExtension
 *
 */
class GeSHiExtended extends GeSHi {  
  /**
   * @var This variable is just used to call function that should be static
   */
  private static $emptyGeshiSingleton ;
  
  /**
   * A empty geshi object to be used only for global function call
   * @return GeSHi
   */
  public static function getEmptyGeshiSingleton() {
    if (!isset(self::$emptyGeshiSingleton)) {
      self::$emptyGeshiSingleton = new GeSHi() ;
    }
    return self::$emptyGeshiSingleton ;
  }
  
  /*----------------------------------------------------------------------------------------
   *   Schema of a geshi language file
   *----------------------------------------------------------------------------------------
   *
   * Languages files contain information of different kind. There is no explicit definition
   * of the schema of GeSHi language files. The constants and functions below aims to cope with
   * this issue so that some rather generic treatments (such as analysis) can be done on the
   * overall schema. Note that the elements below are static as they describe GeSHi schema,
   * rather than a particular language expressed using this schema.
   */
  
  /**
   * @var Map(String,String) This constants defines the fields that could appear
   * in geshi language definition files as well as their type.
   * This constant value is not to be directly accessed. Use getFieldInfo() instead.
   */
  private static $languageDescriptionSchema = array(
    'LANG_NAME'        => "STR",
    'CASE_KEYWORDS'    => "BOOL",
    'CASE_SENSITIVE'   => "INT=>BOOL",
    'COMMENT_SINGLE'   => "INT=>REG",
    'COMMENT_MULTI'    => "REG=>REG",
    'COMMENT_REGEXP'   => "INT=>REG",
    'ESCAPE_CHAR'      => "STR",
    'ESCAPE_REGEXP'    => "INT=>REG",
    'HARDQUOTE'        => "INT=>REG",
    'HARDCHAR'         => "STR",
    'HARDESCAPE'       => "INT=>REG",
    'HIGHLIGHT_STRICT_BLOCK'=> 'INT=>',
    'KEYWORDS'         => "INT=>INT=>STR",
    'LANG_NAME'        => 'PHP',
    'NUMBERS'          => "ENUM",
    'OBJECT_SPLITTERS' => "INT=>REG",
    'OOLANG'           => "BOOL",
    // 'PARSER_CONTROL'
    'QUOTEMARKS'       => "INT=>REG",
    'REGEXPS'          => "INT=>REG",
    'SCRIPT_DELIMITERS'=> "INT=>INT=>REG",  
    'STRICT_MODE_APPLIES'=>"ENUM",
    'STYLES'           => "ENUM=>(INT|ENUM)=>STR",  
    'SYMBOLS'          => "INT=>INT=>STR",
    'TAB_WIDTH'        => "INT",
    'URLS'             => "INT=>STR" );  

  /**
   * @var Defines the relationships between the class prefix and the corresponding
   * information. This binding is hidden in the GeSHi code.
   * This constant is not expected to be accessed directly.
   */
  
  private static $classShortcuts = array(
      'kw'=>'KEYWORDS', 
      'co'=>'COMMENTS',
      'es'=>'ESCAPE_CHAR',
      'br'=>'BRACKETS',
      'st'=>'STRINGS',
      'nu'=>'NUMBERS',
      'me'=>'METHODS',
      'sy'=>'SYMBOLS',
      'sc'=>'SCRIPT',
      're'=>'REGEXPS' 
  ) ;
  
  /**
   * Return information for a language description field.
   * type LanguageDescriptionFieldInfo == map{
   *   'name' => String!,
   *   'kind' => FieldKind!,
   *   'type' => String  // see $languageDescriptionSchema for the format
   * }
   *   
   * type FieldKind == 'mapOfMap'|'map'|'scalar'
   * @return 
   */
  private static function getFieldSchema($fieldName) {
    if (isset(self::$languageDescriptionSchema[$fieldName])) {
      $r = array() ;
      $type=self::$languageDescriptionSchema[$fieldName] ;
      $nbfun = count(explode('=>',$type)) ;
      if ($nbfun===2) {
        $kind = "mapOfMap" ;
      } elseif ($nbfun===1) {
        $kind = "map" ;
      } else {
        $kind = "scalar" ;
      }
      $r['name'] = $fieldName ;
      $r['type'] = $type ;
      $r['kind'] = $kind ;
      return $r ;
    } else {
      die("GeSHiExtended.getFieldInfo: $fieldName is not a field") ;
    }  
  }
  
  /**
   * Return the schema of geshi files.
   * type LanguageDescriptionSchema == map+(String!,LanguageDescriptionFieldInfo)
   * @return LanguageDescriptionSchema
   */
  public static function getGeshiSchema() {
    $r=array() ;
    foreach(array_keys(self::$languageDescriptionSchema) as $field) {
      $r[$field] = self::getFieldSchema($field) ;
    }
    return $r ;
  }
  
  
  public static function getFullTokenClassName($classname) {
    $shortcut = substr($classname,0,2) ;
    if(isset(self::$classShortcuts[$shortcut])) {
      return self::$classShortcuts[$shortcut] ;
    } else {
      if ($shortcut==='de') {
       // this is a trick used by the tokens functions in SourceCode.
       // if a regular text is not in a span it returns 'de...'
       return 'OTHER' ;
      } else {
       return $classname ;
      }
    }
  }
  
  /*----------------------------------------------------------------------------------------
   *   Language descriptions
   *----------------------------------------------------------------------------------------
   * The elements above meant to deal with Geshi schema. Below the goal is to provides
   * function to deal with language description conforming to this schema and adding
   * additional information such as metrics.
   */
  
  /**
   * Return for a given language its description, that is the information in
   * the geshi language file plus a summary.
   * 
   * type FieldValueDescription == Map {
   *   'name'  : String!,       // The geshi language code
   *   'geshi' : NestedArray,   // The structure of this array conforming to LanguageDescriptionSchema
   *                            // that is, this is the content of the geshi language file
   *   'summary' : NestedArray? // A summary computed via the valueSummary() function. 
   *                            // This is an array. If nothing is interesting then this value is not defined. 
   * }
   * @param $language geshi language code
   * 
   * @return Map(String!,FieldValueDescription)! for each field its field value description.
   */
  public static function getLanguageDescription($language) {
    $geshi = new GeSHiExtended() ;
    $geshi->set_language($language,true) ;
    $languageData = $geshi->language_data ;
    $analysis=array() ;
    foreach (self::getGeshiSchema() as $field => $fieldInfo) {
      if (isset($languageData[$field])) {
        $analysis[$field]['name']=$field ;
        $analysis[$field]['geshi']=$languageData[$field] ;
        $summary= valueSummary($languageData[$field],"*empty*") ;
        if ($summary !== "*empty*" && is_array($summary)) {
          $analysis[$field]['summary']=$summary ;
        }
      }
    }
    return $analysis ;
  }
  
  /**
   * Return all language descriptions. Use var_dump to see the structure.
   * @return Map*(String,LanguageDescription!)
   */
  public static function getAllLanguageDescriptions() {
    $r = array() ;
    $geshi = new GeSHiExtended() ;
    $languages = $geshi->get_supported_languages() ;
    //echo count($languages). " languages descriptions founded" ;
    foreach($languages as $language) {
      // echo "Loading language $language..." ;
      $r[$language] = self::getLanguageDescription($language) ;
      // echo "done <br/>" ;
    }
    return $r ;
  }
  
  /**
   * Return a matrix that can be displayed via mapOfMapToHTMLTable
   * @return Map(LanguageCode,Map(LanguageProperty,Value))
   */
  public static function getLanguageProperties() {
    $allLanguageDescriptions=self::getAllLanguageDescriptions() ;
    $languageProperties=array() ;
    foreach($allLanguageDescriptions as $language => $languageDescription) {
      foreach($languageDescription as $field => $fieldValueDescription) {
        if (isset($fieldValueDescription['summary'])) {
          $arr = unnest_array($fieldValueDescription['summary'],' ') ;
          foreach($arr as $key => $value) {
            $languageProperties[$language][$field.' '.$key]=$value ;
          }
        } else {
          // this is an atomic value
          $languageProperties[$language][$field]=$fieldValueDescription['geshi'] ;
        }
      }
    }
    return $languageProperties ;
  }
  
  /**
   * Return a HTML matrix with one line for each language and one column for
   * each properties. The list of properties to be displayed can be specified.
   *  
   * @param false|true|RegExp|List*(String!*)? $propertySpec
   * If false there will be no header (no special first row) but all columns are included.
   * If true the first row is a header, and all columns are included.
   * If a string is provided then it is assumbed to be a regular expression. Only matching
   * column names will be added to the table.
   * If $displayFilter is a list, this list will constitute the list of columns headers.
   * Default is true.
   * 
   * @return HTMLTable The HTML of a table
   */
  public static function getLanguagePropertyHTMLMatrix($propertySpec=true) {
    return mapOfMapToHTMLTable(self::getLanguageProperties(),'',$propertySpec,true,null,$border="2") ;
  }
  
  
  /**
   * Return the language suggested by geshi for a given extension (without .)
   * or '' if nothing is suggested.
   */
  public static function getLanguageFromExtension($extension) {
    $g = self::getEmptyGeshiSingleton() ;
    return $g->get_language_name_from_extension($extension) ;
  }
  
  public function __construct() {
    parent::__construct() ;
  }
}









define('MAX_LINE_LENGTH',1000) ;
define('MAX_NB_OF_LINES',10000) ;

/**
 * Model source code. By contrast to SourceFiles.php which deals with files containing
 * SourceCode here, only the some text is given as well as the language in which it
 * is written (as a GeSHi language code).
 * This class provides support for source code analysis, manipulation, display, etc.
 * It is based on the GeSHI libraries that allows both generation of html
 * code but also raw lexical analysis for many different languages thanks to the
 * geshi language definitions.
 * 
 * The class deals with 4 representations of a source code
 * - a plain textual version
 * - an html version generated by geshi
 * - an xml version of the html used for xpath queries 
 * - a token sequence representation based on xml
 */
class SourceCode {
  

  /*-------------------------------------------------------------------------
   *   Fields
   * ------------------------------------------------------------------------
   */
  
  /**
   * @var String|false the last error generated by this class.
   * There is no need to change this state in case of a geshi error
   * (see getError).
   */
  protected $error = false ;
  
  
  /**
   * @var String! A unique code that is used in particular as a prefix of html ids
   * when various source code are to be displayed in the same page. This allow 
   * different css styling for different source code on the same page.
   * If this code is not explicitely provided then is is automatically generated.
   */
  protected $sourceId ;
  
  /**
   * @var an integer used for the automatic generation of sourceIds.
   * This variable is global and represents the next available number.
   */
  private static $nextIdAvailable = 0 ;
  
  /**
   * Return a new generated source id
   * @return String! a new source id 
   */
  private static function getNewSourceId() {
    $id = SourceCode::$nextIdAvailable ;
    SourceCode::$nextIdAvailable = $id+1 ;
    return "s$id" ;
  }
    
  /**
   * @var String! the source code as a regular string
   */
  protected $plainSourceCode ;
  
  
  
  
  
  /**
   * @var String! language string used by the geshi package for highlighting
   */
  protected $geshiLanguage ;

  /**
   * @var GeSHI? the geshi object used for highlighting. Computed on demand.
   */
  protected $geshi = null;
  
  /**
   * @var HTML? the html version of the highlighted source code. Computed on demand.
   */
  protected $geshiHtmlSourceCode ;
  
  /**
   * @var SimpleXMLElement? The XML representation of htmlSourceCode source code, computed on demand. 
   */
  protected $geshiXMLSourcCode ;
  
  /**
   * Array of text node, that is a list of list of text node,
   * when the first level corresponds to source lines, and next level
   * to the line of text nodes. In fact, this structure helps in downgrading the
   * complexity of geshi which does not provide in fact a simple
   * list of tokens, but some nested span sometimes. Here only text nodes
   * are kept, along with the class in which they appear.
   * 
   * type TextNode == Map{
   *        'rawText' => String!,      // the raw value of text node
   *        'rawClass' => String!,     // the raw value of class embedding the text node
   *        'domNode' => DOMNode!     // Node of type XML_TEXT_NODE
   *   }
   * type TextNodeArray == List*(List*(TextNode!))  // one for each line in the source code
   * 
   * @Var TextNodeArray? The array of text nodes, computed on demand.
   */
  protected $textNodeArray = null ;
  
  
  /**
   * @var unknown_type
   */
  protected $inlineFragmentMap = array() ; 
    
  
  /*-------------------------------------------------------------------------
   *  Error 
   *-------------------------------------------------------------------------
   */
  
  /**
   * Returns an error message associated with the last GeSHi operation,
   * or false if no error has occured
   *
   * @return string|false An error message if there has been an error, else false
   * @since  1.0.0
   */
  public function error() {
    $geshiError = $this->getGeSHI()->error() ;
    if ($geshiError) {
      return $geshiError ;
    } else {
      return false ; $error ;
    }
  }
  
  /*-------------------------------------------------------------------------
   *   Plain textual view Views
   * ------------------------------------------------------------------------
   */
  
  
  /**
   * Return the plain source code as is.
   * @return String! The source code as a string.
   */
  public function getPlainSourceCode() {
    return $this->plainSourceCode ;
  }
  
  public function getGeshiLanguage() {
    return $this->geshiLanguage ;
  }
  
  /*-------------------------------------------------------------------------
   *   HTML Views
   * ------------------------------------------------------------------------
   */

  
  public function releaseMemory() {
    unset($this->geshi) ;
    unset($this->geshiHtmlSourceCode) ;
    unset($this->geshiXMLSourcCode) ;
    unset($this->textNodeArray) ;
  }
  
   
  
  public function getSourceId() {
    return $this->sourceId ;
  }

  
  /**
   * Get a geshi object for this source. This function is for internal use.
   * @return GeSHI! The geshi object associated with the source.
   */
  protected function getGeSHI() {
    if (!isset($this->geshi)) {
      
      // truncante long lines and limit the number of lines
      $text = "" ;
      $linesTruncated=array() ;
      $lines = explode("\n",$this->plainSourceCode) ;
      $nbOfLines = count($lines) ;
      // echo $nbOfLines ;
      $n = 0 ;
      while ($n < $nbOfLines && $n < MAX_NB_OF_LINES) {
        $line = $lines[$n];
        if (strlen($line)>MAX_LINE_LENGTH) {
          $msg =
            "line #".($n+1)." has been truncated to "
            .MAX_LINE_LENGTH." characters (out of ".strlen($line)." characters)\n" ;          
          $lines[$n] = substr($lines[$n],0,MAX_LINE_LENGTH)."... TRUNCATED" ;
          echo $msg ; 
        }
        $text .= $line."\n" ;
        $n++ ;
      }
      if (count($linesTruncated)) {
        $text = "WARNING: Some long lines have been truncated."
                 ."The file might not display correcly\n"
                 .$text ;
      }
      $text = implode("\n",$lines) ;
      if ($nbOfLines > MAX_NB_OF_LINES) {
        $msg = "\nFILE truncated to ".MAX_NB_OF_LINES." lines (out of ".$nbOfLines." lines)\n" ;
        $text .= $msg ;
        echo $msg ;
      }
      
      $geshi = new GeSHi() ;
      $geshi->set_source($text) ;
      $geshi->set_language($this->geshiLanguage) ; 
      $geshi->set_overall_id($this->sourceId) ;
      $geshi->enable_line_numbers(GESHI_NORMAL_LINE_NUMBERS) ;
      $geshi->enable_classes();
      $geshi->enable_ids(true);
      $this->geshi = $geshi ;
    }
    return $this->geshi ;
  }
  
  /**
   * Return the source code as a raw html string. 
   * (no line numbers, no higlighting, preformatted only).
   * @return HTML!
   */
  public function getRawHTML() {
    return htmlAsIs($this->source) ;
  }

  
  /**
   * An html version of the source code. This HTML code contains classes and ids
   * that could be used by the CSS. The HTML return here is not a document.
   * That is CSS should  be included before in the header of the document if it is to 
   * be displayed.
   * Otherwise it can be also be used as a HTML fragment and served as a service.
   * @return HTML!
   */
  public function getHTML() {
    if (!isset($this->geshiHtmlSourceCode)) {
      
      $geshi = $this->getGeSHI() ;
      $html = $geshi->parse_code();
      // for some reason we should remove the caracters below to avoid problem
      // when converting this html to xml.
      $this->geshiHtmlSourceCode = str_replace('&nbsp;',' ',$html) ;
    }
    return $this->geshiHtmlSourceCode ;
  }
  
  /*-------------------------------------------------------------------------
   *   CSS Styling
   * ------------------------------------------------------------------------
   */
  
  
  /**
   * Return the geshi standard CSS associated with the language.
   * @CSS! the CSS string 
   */
  public function getStandardCSS() {
    return $this->getGeSHI()->get_stylesheet();
  }
  
  /**
   * Return the CSS statements useful to emphasise a particular set of lines.
   * This CSS string could be used in conjuction with the standard CSS.
   * @param RangeString? $lines the set of lines to emphasize.
   * $lines is a string of the form '2-4,5,17-28'
   * (@see rangesExpression in Strings.php). Default to an empty string
   * in which case nothing is produced.
   * @param $style a list of CSS attribute assignement used to emphasize
   * the fragment.
   * @Return CSS! A CSS string
   */
  public function getFragmentCSS($lines='',$style='background:#FFAAEE;') {    
    $css='' ;
    $idprefix='#'.$this->sourceId.'-' ;
    $ids = $idprefix.implode(','.$idprefix,rangesExpression($lines)) ;
    if ($ids!='') {
      $css .= $ids. ' { '.$style.' }' ;
    }
    return $css ;
  }
    
  
  /**
   * Return the CSS that is necessary to style the html code with the
   * possibility the emphasize particular lines.
   * @param RangeString? if specified $lines represents the set of lines that
   * should be emphasized. This could be useful to show a code fragment.
   * $lines is a string of the form '2-4,5,17-28'
   * (@see rangesExpression in Strings.php). Default to an empty string,
   * that is by default no lines are emphasised.
   * @Return CSS! A CSS string that contains both regular geshi stylesheet
   * and
   */
  public function getCSS($lines='',$style='background:#FFAAEE;') {
    $css = $this->getStandardCSS() ;
    $css .= $this->getFragmentCSS($lines,$style) ;
    return $css ;
  }
  
  
  /**
   * Return a simple HTML header that include the CSS generated with getCSS.
   * This function could be used for simple HTML documents with one source.
   * @param RangeString? $lines
   * @param unknown_type $style
   * @return string
   */
  public function getHTMLHeader($lines='',$style='background:#FFAAEE;') {
    return '<html><head><title>Code</title><style type="text/css"><!--'
           .$this->getCSS($lines,$style)
           .'--></style></head>' ;
  }
    

  
  
  /*-------------------------------------------------------------------------
   *   XML view
   * ------------------------------------------------------------------------
   */
  
  
  /**
   * Return the source code as XML geshi representation.
   * This function is for internal usage. 
   * @return DOMDocument! The dom representation of the geshi representation
   */

  
  public function getXML() {
    if (!isset($this->geshiXMLSourceCode)) {
      $document=new DomDocument() ;
      if($document->loadHTML($this->getHTML())===false) {
        die('error: HMTL produced by GeSHi is not valid XML') ;
      } else {
        $this->geshiXMLSourceCode = $document ;
      }
    }
    return $this->geshiXMLSourceCode ;
  }
  
  
  /**
   * Returns elements of a given type and given html class
   * @param String $classname
   * @return List*(SimpleXMLElement) the list of nodes corresponding to the given class
   */

  public function getXMLElements($element='span',$classname="") {
      $doc = $this->getXML() ;
      $xpath = new DOMXPath($doc) ;
      if ($classname==="") {
        $xpathExpr = '' ;
      } else {
        $xpathExpr = '[@class="'.$classname.'"]' ;
      }
      return $xpath->query('//'.$element.$xpathExpr) ;
  }


  /*-------------------------------------------------------------------------
   *   Tokens view
   * ------------------------------------------------------------------------
   */
  
  /**
   * Return for a given node, the list of TextNode found at any level with 
   * corresponding decoration (@see TextNode).
   * This function is for internal use only, it deals with the fact that the line
   * is not a flat list of nodes, but instead a list of trees. 
   * @param DOMNode $node initially the node corresponding the line node. But since
   * the function it is recursive it will be called for arbitrary node.
   * @return List*(TextNode!)! the list of text nodes.
   */
  private function getTextNodes($node) {
    switch ($node->nodeType) {
      case XML_TEXT_NODE:
        // this is a regular text. No problem, we get it.
        $text  = $node->nodeValue ;
        $class = $node->parentNode->getAttributeNode('class')->nodeValue ;
        return 
          array(
            array(
              'rawText'=>$text,
              'rawClass'=>$class,
              'domNode'=>$node)) ;
        break ;
      case XML_ELEMENT_NODE:
        // this is a tree. Go into it and get tokens.
        $r = array() ;
        foreach($node->childNodes as $child) {
          $r = array_merge($r,$this->getTextNodes($child)) ;
        }
        return $r ;
        break ;
      default:
        // we don't care about other kind of nodes
    }
  }
  
  
  /**
   * Return the source code as a TextNodeArray.
   * @return TextNodeArray? 
   */
  public function getTextNodeArray() {
    if (!isset($this->textNodeArray)) {
      $nline=0 ;
      $this->textNodeArray=array();
      
      // for each lines
      foreach($this->getXMLElements('li','li1') as $lineNode) {
        $nline++ ;
        $this->textNodeArray[$nline] = array() ;
        
        // for each text node in this line 
        foreach($this->getTextNodes($lineNode) as $textNode) {
          $this->textNodeArray[$nline][]=$textNode ;    
        }
      }
    }
    return $this->textNodeArray ;
  }
  
  
  
  /**
   * Return the list of tokens corresponding to some criteria.
   * 
   * Token == Map{
   *   'text' => NonEmptyString,
   *   'class' => String,
   *   'line' => Integer >= 1,
   *   'i' => Integer >= 1    // index of the token on the line
   * }
   * 
   * @param RegExpr $classExclude the token whose class match this regexpr
   * will be ignored. Default to /co/ meaning that comments are ignored.
   * To ignore strings as well /co|st/ can be used. It might be also usefull
   * to remove escape char with /so|st|es/. In fact, the usage of the classes
   * depends on the language description.
   *
   * @param Boolean? $trimClassExclude indicates for which token class text should not
   * be trimmed. If '/-/' is specified then all token texts will be trimmed
   * as no classes are excluded. That is leading and trailing spaces will be
   * removed. If this results in an empty string, then the token will be removed. 
   * Default to /st|es/ that is all tokens that are not either a string or
   * a escaped character with be trimmed.
   *
   * @param RegExpr $shortClassName indicates if the class names should be
   * shorten to two letters. That is instead of having 'co1', 'co2', etc. the
   * class will be just 'co'. Note that the filters are still applied before
   * this truncation. Default is true.
   *
   * @return List*(Token)! The list of token selected.
   */
  
  public function getTokens($classExclude='/co/',$trimClassExclude='/st|es/',$shortClassName=true) {
    $tokens=array();
    $array=$this->getTextNodeArray() ;
    
    // for each lines
    foreach($array as $lineNo => $textNodeList) {
      // for each token in the line
      foreach($textNodeList as $textNodeNo => $textNode) {
        $token=array() ;
        // get the text
        if (!preg_match($trimClassExclude,$textNode['rawClass'])) {
          $token['text']=trim($textNode['rawText']) ;
        } else {
          $token['text']=$textNode['rawText'] ;
        }
        // get the class
        if ($shortClassName) {
          $token['class']=substr($textNode['rawClass'],0,2) ;
        } else {
          $token['class']=$textNode['rawClass'] ;
        }
        // get coordinates
        $token['line']=$lineNo ;
        $token['i']=$textNodeNo ;
        // add the token or node
        if ($token['text']!=='' && !preg_match($classExclude,$textNode['rawClass'])) {       
          $tokens[]=$token ;
        }
      }
    }
    return $tokens ;
  }
 
  /**
   * Generate a string representing a given token
   * @param Token! $token the token
   * @param String! $tokenPartSeparator if '' only the text of the token will be returned.
   * Otherwise each token attribute will be separated with this separator.
   * @return String! the string corresponding to the token
   */
  public static function tokenToString($token,$tokenPartSeparator=':') {
    if ($tokenPartSeparator==='') {
      return $token['text'] ;
    } else {
      return implode($tokenPartSeparator,array($token['text'],$token['class'],$token['line'],$token['i'])) ;
    }
  }
  
  /**
   * @param Tokens! $tokens the list of token
   * @param String! $tokenPartSeparator if '' only the text of the token will be returned.
   * Otherwise each token attribute will be separated with this separator.
   * @return String! the string corresponding to the token

   * @param unknown_type $tokens
   * @param String! $tokenPartSeparator
   * @param String! $tokenSeparator
   * @return string
   */
  public static function tokensToString($tokens,$tokenPartSeparator='',$tokenSeparator="\t") {
    $r='' ;
    foreach($tokens as $token) {
      $r[]=self::tokenToString($token,$tokenPartSeparator) ;
    }
    return implode($tokenSeparator,$r) ;
  }
  
  
    
  /*-------------------------------------------------------------------------
   *   Metrics
   * ------------------------------------------------------------------------
   */
      
  
  /**
   * Total number of lines (comments and blank lines included).
   * @return Integer > 0
   */
  public function getNLOC() {
    return count(explode("\n",$this->plainSourceCode)) ;
  }
  
  /**
   * Return a summary of the source analysis including token frequencies and lines number.
   * If a list of tokens is provided than the summary is based on this list, otherwise
   * compute the summary on the default list of tokens.
   * 
   * type ClassFrequencies == Map{
   *     'sum'      => Integer>=1,  // the total number of token occurences
   *     'distinct' => Integer>=1,  // the number of different tokens
   *     'min'      => Integer>=1,  // the minimum of token occurences
   *     'max'      => Integer>=1,
   *     'tokens'   => Map(String!,Integer>=1)  // the frequency of each token
   *   }
   *   
   * type SourceCodeSummary == Map{
   *     'sourceId' => String!,          // an id used to distinguish different source code in a same page.
   *     'geshiLanguage' => String!,     // the geshi language 
   *     'frequencies' =>                // for each token class the corresponding frequencies of tokens
   *       Map(String!,ClassFrequencies), 
   *     'nloc' => Integer >= 0          // number of line of code 
   *     'ncloc' => Integer >= 0         // nb of lines that contains at least a non comment token.
   * @param unknown_type $tokens
   * @return multitype:number Ambigous <multitype:, mixed> 
   */
  public function getSummary($tokens=null) {
    if ($tokens===null) {
      $tokens=$this->getTokens() ;
    }
    $frequencies=array() ;
    $nonCommentedLines[]=array() ;
    foreach($tokens as $token) {
      $class=$token['class'] ;
      $text=$token['text'] ;
      if (isset($frequencies[$class]['sum'])) {
        $frequencies[$class]['sum']++ ;
        if (isset($frequencies[$class]['tokens'][$text])) {
          $frequencies[$class]['tokens'][$text]++ ; 
        } else {
          $frequencies[$class]['tokens'][$text]=1;
        }
      } else {
        $frequencies[$class]['sum']=1 ;
        $frequencies[$class]['tokens'][$text]=1 ;
      }
      if (!startsWith($class,'co')) {
        $nonCommentedLines[$token['line']]=true;
      }
    }
    foreach($frequencies as $class=>$map) {
      $frequencies[$class]['distinct']=count($frequencies[$class]['tokens']) ;
      $frequencies[$class]['min']=min($frequencies[$class]['tokens']) ;
      $frequencies[$class]['max']=max($frequencies[$class]['tokens']) ;
    }
    return array(
      'sourceId'      => $this->getSourceId(),
      'geshiLanguage' => $this->getGeshiLanguage(),
      'frequencies'   => $frequencies,
      'size'          => strlen($this->plainSourceCode),
      'ncloc'         => count($nonCommentedLines),
      'nloc'          => $this->getNLOC() ) ;
  }
  
  /**
   * Return a simplified and flatten version of the summary.
   * Token frequencies have been removed 
   * @return Map(String!,String|Integer)!
   */
  public static function simplifiedSummary($summary) {
    $r = $summary ;
    $frequencies=$summary['frequencies'] ;
    unset($r['frequencies']) ;
    foreach ($frequencies as $classshortcut => $map) {
      $classfullname = GeSHiExtended::getFullTokenClassName($classshortcut)  ;
      foreach ($map as $key => $value) {
        if (!is_array($value)) {
          $r[$classfullname.' '.$key]=$value ;
        }
      }
    }
    return $r ;
  }
  
  /**
   * Return both the summary and the list of tokens as a Json string.
   * @see getSummary and getTokens for the documentation
   * @return Json!
   */
  
  public function getTokensAsJson(
      $classExclude='/co/',
      $trimClassExclude='/st|es/',
      $shortClassName=true)  {
    $tokens = $this->getTokens($classExclude,$trimClassExclude,$shortClassName) ;
    return json_encode($tokens) ; 
  }
   
  
  /**
   * Create a source code.
   * 
   * @param String! $text The text representing the source code
   * 
   * @param GeshiLanguage! $language The geshiLanguage in which this source code is written
   * 
   * @param String? $sourceid an optional sourceId that will be used to differentiate this source 
   * from other sources if in the same html page. This will be used as a CSS class name and prefix
   * for CSS id, so it should be short. If nothing is provided an identifier will be automatically
   * generated. This is probably the best.
   */
  public function __construct($text,$geshiLanguage,$sourceid=null) {
    $this->plainSourceCode = $text ;
    $this->geshiLanguage = $geshiLanguage ;
    if (isset($sourceid)) {
      $this->sourceId = $sourceid ;
    } else {
      $this->sourceId = SourceCode::getNewSourceId() ;
    } 
  }
  
}

function startsWith($haystack, $needleOrNeedles){
  if (is_string($needleOrNeedles)) {
    $needles = array($needleOrNeedles) ;
  } else {
    $needles = $needleOrNeedles ;
  }
  foreach ($needles as $needle) {
    if (substr($haystack, 0, strlen($needle)) === $needle) {
      return true ;
    }
  }
  return false ;
}






