<?php

/*  Function:   convert_number
**  Arguments:  int
**  Returns:    string
**  Description:
**      Converts a given integer (in range [0..1T-1], inclusive) into
**      alphabetical format ("one", "two", etc.).
*/
function convert_number($number)
{
    if (($number < 0) || ($number > 999999999))
    {
        return "$number";
    }

    $Gn = floor($number / 1000000);  /* Millions (giga) */
    $number -= $Gn * 1000000;
    $kn = floor($number / 1000);     /* Thousands (kilo) */
    $number -= $kn * 1000;
    $Hn = floor($number / 100);      /* Hundreds (hecto) */
    $number -= $Hn * 100;
    $Dn = floor($number / 10);       /* Tens (deca) */
    $n = $number % 10;               /* Ones */

    $res = "";

    if ($Gn)
    {
        $res .= convert_number($Gn) . "Million";
    }

    if ($kn)
    {
        $res .= (empty($res) ? "" : " ") .
            convert_number($kn) . "Thousand";
    }

    if ($Hn)
    {
        $res .= (empty($res) ? "" : " ") .
            convert_number($Hn) . " Hundred";
    }

    $ones = array("", "One", "Two", "Three", "Four", "Five", "Six",
        "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
        "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eightteen",
        "Nineteen");
    $tens = array("", "", "Twenty", "Thirty", "Fourty", "Fifty", "Sixty",
        "Seventy", "Eigthy", "Ninety");

    if ($Dn || $n)
    {
        if (!empty($res))
        {
            $res .= "and";
        }

        if ($Dn < 2)
        {
            $res .= $ones[$Dn * 10 + $n];
        }
        else
        {
            $res .= $tens[$Dn];

            if ($n)
            {
                $res .= $ones[$n];
            }
        }
    }

    if (empty($res))
    {
        $res = "zero";
    }

    return $res;
}

function getItemizedTex($markup){
    return $markup;
    
  if($markup == '') return $markup;
  
  $tex = PHP_EOL . "\\begin{itemize}";
  foreach(explode(PHP_EOL, $markup) as $line) {
    if($line != '') {
      //$t = formatter::toTex($line);
      //$t1 = formatter::toPlainText($t); //hadnle remaining wiki markup
     // if($t == $line){
     //    $tex .= PHP_EOL . "\\item \\wikiref{}{}". $t1;
    //  }
    //  else{
           $tex .= PHP_EOL . "\\item ". $line;
    //  }   
    }
  }
  $tex .=  PHP_EOL . "\\end{itemize}" . PHP_EOL;
  return $tex;
}

function handleUmlauts($txt){
 $txt = str_replace("ä", "\\\"{a}", $txt);
 $txt = str_replace("ö", "\\\"{o}", $txt);
 $t = str_replace("ü", "\\\"{u}", $txt);
 return $t;
}

function handleWikiRef($txt){
    $res = str_replace(" ", "_", $txt);
    return $res;
}

function getTexCommandName($txt){
 //var_dump($txt);
 for($i=1000; $i>=0; $i--){
  $str = (string)$i;
  if(strlen(strstr($txt,$str))>0){
    $word = convert_number($i);
    $txt = str_replace($str, $word, $txt);
    //break;
   }
  }

  $txt = str_replace(".", "dot", $txt);
  $txt = str_replace("-", "", $txt);
  $txt = str_replace("/", "", $txt);
  $txt = str_replace("ä", "ae", $txt);
  $txt = str_replace("ü", "ou", $txt);
  $txt = str_replace("ö", "oe", $txt);
  $txt = str_replace(":", "", $txt);
  $res = str_replace(' ', '',$txt);
  return $res;
}


function startsWith($suffix, $text) {
    return (strcmp(substr($text, 0, strlen($suffix)),$suffix)===0);
}

function endsWith($haystack,$needle,$case=true) {
      if($case){return (strcmp(substr($haystack, strlen($haystack) - strlen($needle)),$needle)===0);}
      return (strcasecmp(substr($haystack, strlen($haystack) - strlen($needle)),$needle)===0);
}

class formatter{
    public static function toPlainText($text) { 
    
     $pattern =  '/\[\[(:)?((\w|\d|\s|\/|\-|\.|\#)+):((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\2:\4';
     $text = preg_replace($pattern, $replacement, $text);
   
     
     $pattern =  '/\[\[(:)?(((\w|\d|\s|\/|\-|\.|\#)+):)?((\w|\d|\s|\/|\-|\.|\#)+)\|((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\7';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/\[\[((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\1';
     $text =  preg_replace($pattern, $replacement, $text);
     
     $pattern =  $pattern =  '/\[(\S+)\s+\S+\]/';
     $replacement = '\1';
     $text =  preg_replace($pattern, $replacement, $text);
     
    return $text;
   }
   
   public static function handleLinks($text){
    if($text == '') return '';
     if($text == null) return '';
     
     $pattern =  '/\[\[(:)?((\w|\d|\s|\/|\-|\.|\#)+):((\w|\d|\s|\/|\-|\.|\#)+)\|((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\\wikiref{\2:\4}{\6}';
     $text = preg_replace($pattern, $replacement, $text);
    
     //  --- recognize specific links ---
     $pattern =  '/(Technology:)((\w|\d|\s|\/|\-|\.|\#)+)/';
     $replacement = '\\wikitref{\2}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/(Category:)((\w|\d|\s|\/|\-|\.|\#)+)/';
     $replacement = '\\wikiref{Category:\2}{\2}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/(Language:)((\w|\d|\s|\/|\-|\.|\#)+)/';
     $replacement = '\\wikilref{\2}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/(101feature:)((\w|\d|\s|\/|\-|\.|\#)+)/';
     $replacement = '\\wikifref{\2}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/(101implementation:)((\w|\d|\s|\/|\-|\.|\#)+)/';
     $replacement = '\\wikiiref{\2}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/(101contributor:)((\w|\d|\s|\/|\-|\.|\#)+)/';
     $replacement = '\\wikicontribref{\2}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/(101companies:)((\w|\d|\s|\/|\-|\.|\#)+)/';
     $replacement = '\\wikicref{\2}';
     $text = preg_replace($pattern, $replacement, $text);
          
     //----------------------------------------------------------
     
     $pattern =  '/\[\[(:)?((\w|\d|\s|\/|\-|\.|\#)+):((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\\wikiref{\2:\4}{\4}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/\[\[((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\\wikiref{\1}{\1}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/\[\[((\w|\d|\s|\/|\-|\.|\#)+)\|((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\\wikiref{\1}{\3}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $text = escape($text);
     $res = handleUmlauts($text);
       
    // var_dump($res);
     return $res;  
   }
   
   
    public static function handleCites($text){
      $pattern = '/<cite>([^<]*)<\/cite>/';
      $replacement = '\\cite{\1}';
      return preg_replace($pattern,$replacement,$text);
      
    }
   
    public static function sourceLinks($title,$text) {
      $pattern = '/\[this!!(([^\]])+\/)*((\d|\w)+)(\.(\d|\w)+)?( (\d|\w)+(\.(\d|\w)+)*?)?\]/';
      $sfURL = 'https://github.com/101companies/101implementations/blob/master/';
      $sfProject = str_replace('101implementation:','',$title);
      $replacement = '\\begin{small}\\textsf{\\href{'.$sfURL.$sfProject.'/\1'.'\3\5'.'?view=markup}{\3\5}}\\end{small}';
      $newText = preg_replace($pattern,$replacement,$text);
      return $newText;
    }
    
    public static function extLinks($text) {
      $pattern = '/\\[http\:\/\/([^\]]*)\]/';
      preg_match_all($pattern, $text, $matches);
      $links = array();
      foreach($matches[0] as $match){
        array_push($links, str_replace('\\','',str_replace('[','',str_replace(']','',$match))));
      }
      return $links;
    }


    public static function intLinks($tex,$titles){
      foreach ($titles as $title){
        array_push($titles, str_replace('_',' ',$title));
      }
      // general links
      $pattern = '/wikiref{((\d|\w|\:|\s)*)}{((\d|\w|\:|\s)*)}/';
      preg_match_all($pattern,$tex,$matches, PREG_SET_ORDER);
      foreach ($matches as $match){
        if (in_array($match[1],$titles)){
          if (startsWith('101implementation:',$match[1])){
            $tex = str_replace($match[0],"hyperlink{impl".str_replace(' ','',str_replace('101implementation:','',$match[1]))."}{\\textsf{\\textit{".$match[3]."}}}",$tex);
          }
          else {
            $tex = str_replace($match[0],"hyperlink{ttc".str_replace('Technology:','',str_replace(' ','',str_replace('Technology:','',$match[1])))."}{".$match[3]."}",$tex);
          }
        }
      }
      //tech links
      $pattern = '/wikitref{((\d|\w|\:|\s)*)}/';
      preg_match_all($pattern,$tex,$matches, PREG_SET_ORDER);
      foreach ($matches as $match){
        if (in_array('Technology:'.$match[1],$titles)){
          var_dump($match[1]);
          if (startsWith('101implementation:',$match[1])){
            $tex = str_replace($match[0],"hyperlink{impl".str_replace(' ','',str_replace('101implementation:','',$match[1]))."}{".$match[1]."}",$tex);
          }
          else {
            $tex = str_replace($match[0],"hyperlink{ttc".str_replace('Technology:','',str_replace(' ','',str_replace('Technology:','',$match[1])))."}{".$match[1]."}",$tex);
          }
        }
      }   
      
      return $tex;
      
    }

    public static function toTex($text) {
     if($text == '') return '';
     if($text == null) return '';
     //var_dump($text);
                               
     $pattern = '/(\[\[(Category:)((\w|\d|\s|\/|\-|\.|\#)+)\]\])/';
     preg_match($pattern, $text, $out);
     if(count($out) > 0){
        $replacement = '';
        $text = preg_replace($pattern, $replacement, $text);
     }
     
      $pattern =  '/\[\[(:)?((\w|\d|\s|\/|\-|\.|\#)+):((\w|\d|\s|\/|\-|\.|\#)+)\|((\w|\d|\s|\/|\-|\.|\#|\')+)\]\]/';
     $replacement = '\\wikiref{\2:\4}{\6}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/\[\[(:)?((\w|\d|\s|\/|\-|\.|\#)+):((\w|\d|\s|\/|\-|\.|\#)+)\|((\w|\d|\s|\/|\-|\.|\#|\')+)\]\]/';
     $replacement = '\\wikiref{\2:\4}{\6}';
     $text = preg_replace($pattern, $replacement, $text);
    
     //  --- recognize specific links ---
     $pattern =  '/\\[\[(Technology:)((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\\wikitref{\2}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/\\[\[(Language:)((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\\wikilref{\2}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/\\[\[(101feature:)((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\\wikifref{\2}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/\\[\[(101implementation:)((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\\wikiiref{\2}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/\\[\[(101companies:)((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\\wikicref{\2}';
     $text = preg_replace($pattern, $replacement, $text);
          
     //----------------------------------------------------------
     
     $pattern =  '/\[\[(:)?((\w|\d|\s|\/|\-|\.|\#)+):((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\\wikiref{\2:\4}{\4}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/\[\[((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\\wikiref{\1}{\1}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern =  '/\[\[((\w|\d|\s|\/|\-|\.|\#)+)\|((\w|\d|\s|\/|\-|\.|\#)+)\]\]/';
     $replacement = '\\wikiref{\1}{\3}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern = '/\[http\:\/\/(([^\s])*)\s*(.+)\]/';
     $replacement = '\\href{http://\1}{\3}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern = '/\[http\:\/\/(([^\s])*)\]/';
     $replacement = '\\href{http://\1}{http://\1}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $pattern = '/<pre>((\s*|.|\s)*)<\/pre>/';
     preg_match($pattern, $text, $out);
     if(count($out) > 0){
        $fname = uniqid("f") . ".ext";
        global $filesFolder; 
        $f = fopen($filesFolder . $fname, "w+");
        fwrite($f, trim($out[1]));
        fclose($f);
        
        $pattern =  '/<pre>((\s*|.|\s)*)<\/pre>/';
        $replacement = '\lstinputlisting[xleftmargin=20pt]{\texgen/files/' . $fname . "}";
        $text = preg_replace($pattern, $replacement, $text);
     }
     
     $pattern = '/<syntaxhighlight lang=\"make" enclose=\"none\">(.*)<\/syntaxhighlight>/';
     $replacement = '\begin{ttfamily}\1\end{ttfamily}';
     $text = preg_replace($pattern, $replacement, $text);
     
     $sfURL = 'https://github.com/101companies/101implementations/blob/master/';
     $text = str_replace(" line>",">", $text);
     $pattern = '/<syntaxhighlight lang=\"([a-zA-Z]*)\"(\s*(source=\"(.*)\")?\s*)>((\s*|.|\s)*)<\/syntaxhighlight>/'; 
     preg_match_all($pattern, $text, $matches, PREG_SET_ORDER);  
     foreach($matches as $match){
        //var_dump($matches);
        //echo PHP_EOL;
        $fname = uniqid("f") . ".ext";
        global $filesFolder; 
        $sourceText = '';
        if ($match[4] != null && $match[4]!= ''){
          $link = $sfURL.$match[4];
          $name = end(explode('/',$match[4]));
          $sourceText = ', caption={\\href{'.$link.'}{'.$name.'}}';
        }             
        $f = fopen($filesFolder . $fname, "w+");
        fwrite($f, trim($match[5]));
        fclose($f);
        
        $pattern = '<syntaxhighlight lang="' . $match[1] .'"'.$match[2].'>' . $match[5] .'</syntaxhighlight>';

        // removed style attribute from the line below: , style=' . $match[1] . '
        $replacement = '\lstinputlisting[xleftmargin=20pt ' . $sourceText . ']{\texgen/files/' . $fname . "}"; //, language=' . $match[1] .$sourceText. //../../files/

        $text = str_replace($pattern, $replacement, $text);
     }
     /*
     $text = str_replace($pattern, $match[5], $text); //av: quick fix by Thomas
     $text = str_replace('lang="haskell" enclose="none">','lang="haskell">', $text);
     $text = str_replace('lang="haskell"  enclose="none">','lang="haskell">', $text);
     */
     $pattern = '/<syntaxhighlight lang=\"([a-zA-Z]*)\" enclose=\"none\">((\s*|.|:|=|>|<|\s|\(|\)|\[|\]|\{|\})*)<\/syntaxhighlight>/'; 
     preg_match_all($pattern, $text, $matches, PREG_SET_ORDER);
     foreach($matches as $match){
        $pattern = '<syntaxhighlight lang="' . $match[1] .'" enclose="none">' . $match[2] .'</syntaxhighlight>';   
        $replacement = '\begin{ttfamily}'.$match[2].'\end{ttfamily}';    
        $text = str_replace($pattern, $replacement, $text);
	}
     
     $text = str_replace('&','\&',$text);
           
     $text = str_replace('<nowiki>','',str_replace('</nowiki>','',$text)); 
     $text = str_replace('$','\$',$text);
     $text = formatter::handleCites($text); 
     $text = formatter::handleBoldAndItalicSpecialCase($text); //we need this because regex cannot handle -> '''                     
     $text = formatter::italic2Textit($text); 
     $text = formatter::handleBold($text); 
	 
     $text = str_replace('->','$\rightarrow$',$text);
     $text = str_replace('=>','$\Rightarrow$',$text); 
     $text = str_replace('<','$<$',$text);
     $text = str_replace('>','$>$',$text);
     
     $text = str_replace('%','\%',$text);   
     
     $text = str_replace("<references>", "", $text);
     $text = str_replace("<references/>", "", $text);
     $text = str_replace('^','\^', $text);
          
     $text = formatter::nestedList($text);
     $text = formatter::subsubsubsections($text);                                                
     $text = formatter::subsubsections($text);
     
     
     $text = escape($text);      
     $res = handleUmlauts($text);
     
     //var_dump($res);
     return trim($res);  
   }
   
    function handleBoldAndItalicSpecialCase($tex){
	 $pattern =  '/\'\'\'((\w*|\W*|\d*|\s*|\-*|\:*|\[*|\]|\|*|\}*|\{*|\\*)*)\'\'\'/'; //'/\'\'(.*)\'\'/';
	 $replacement = '\\textit{\textbf{\1}}';
	 return preg_replace($pattern, $replacement, $tex);
    }

    function italic2Textit($text){
      $newText = '';
      foreach(preg_split( '/\r\n|\r|\n/', $text) as $line) {
        if (startsWith("''",trim($line)) && endsWith(trim($line),"''")){
          $newText .= '\\noindent '.str_replace("''",'','\\textit{'.$line.'}').PHP_EOL;
        } else
          $newText .= $line.PHP_EOL;
        
      }      
      $pattern =  '/\'\'(([^\'])+)\'\'/'; //'/\'\'(.*)\'\'/';
      $replacement = '\\textit{\1}';
      return preg_replace($pattern, $replacement, $newText);
   
    }
    
    function handleBold($text){
     if (startsWith('\'',$text)){
     	echo 'WAS PREFIX';
     	$text = 'REPLACETHISINTEXTP '.$text;
     }
     if (endsWith('\'', $text)){
     	echo 'WAS SUFFIX';
     	$text = $text.' SREPLACETHISINTEXT';
     }
     $pattern =  '/\s\'(([^\'])+)\'\s/'; //'/\'\'(.*)\'\'/';
     $replacement = '\\textbf{\1}';
     $text = preg_replace($pattern, $replacement, $text);;
     $text = str_replace('REPLACETHISINTEXTP ','',$text);
     return str_replace(' SREPLACETHISINTEXT','',$text);
     
    }
     
    
     function subsubsections($text){
      $newText = '';
      foreach(preg_split( '/\r\n|\r|\n/', $text) as $line) {
        if (startsWith("===",trim($line)) && endsWith(trim($line),"===")){
          $newText .= '\\subsubsection'.str_replace("===",'','{'.$line.'}').PHP_EOL;
        } else
          $newText .= $line.PHP_EOL;
        
      }      
      return $newText;
    }  
    
    function subsubsubsections($text){  
      $lines = preg_split( '/\r\n|\r|\n/',$text);
      $newText = '';
      $pattern ='/====(.*)====/';
      $replacement ='\\paragraph{\1}'; 
      foreach ($lines as $line) { 
        if (startsWith('====',$line)){
          $newText .= preg_replace($pattern, $replacement, $line).PHP_EOL;
        } else {
          $newText .= $line.PHP_EOL;
        }
      }         
      return $newText;
    }  
    
    function nestedList($text) {
      //$hasCB = false;
      //if (endsWith($text,"}")) {
      //  $text = substr($text, 0, strlen($test) - 1);
      //  $hasCB = true;
      //} 
      $lines = preg_split('/\r\n|\r|\n/',$text);
      $newText = '';
      $nestLevel = 0;
      $currentNestLevel = 0;
      $newLines = array();
      foreach($lines as $line) {
        $currentNestLevel = strlen(preg_replace('/(\**)\s*(.*)/','\1',$line));
        
        $itemText = preg_replace('/(\**)(.*)/','\2',$line);
        
        // nesting gets depper
        if ($currentNestLevel > $nestLevel) {
            for ($i = 0; $i < $currentNestLevel - $nestLevel; $i++)
              array_push($newLines,'\\begin{itemize'.str_repeat('i',$nestLevel + $i + 1).'}');
            array_push($newLines,'\\item'.$itemText);       
        }
        
        // same or less nesting
        if ($currentNestLevel <= $nestLevel) {
            for ($i = 0; $i < $nestLevel - $currentNestLevel; $i++)
              array_push($newLines,'\\end{itemize'.str_repeat('i',$nestLevel - $i).'}');
            if ($currentNestLevel != 0)
              array_push($newLines,'\\item'.$itemText);
            else
              array_push($newLines, $itemText);
        }
        
        $nestLevel = $currentNestLevel;
      }
      
      for ($i = 0; $i < $nestLevel; $i++)
         array_push($newLines,'\\end{itemize'.str_repeat('i',$nestLevel - $i).'}');
        
      $outText = implode(PHP_EOL,$newLines);
      
        return $outText;
        
   }     
 
}
   
pprint("");
function pprint($text){
  $keys = array("FilePath","IOError","abs","acos","acosh","all","and","any","appendFile","approxRational","asTypeOf","asin","
		asinh","atan","atan2","atanh","basicIORun","break","catch","ceiling","chr","compare","concat","concatMap","
		const","cos","cosh","curry","cycle","decodeFloat","denominator","digitToInt","div","divMod","drop","
		dropWhile","either","elem","encodeFloat","enumFrom","enumFromThen","enumFromThenTo","enumFromTo","
		error","even","exp","exponent","fail","filter","flip","floatDigits","floatRadix","floatRange","floor","
		fmap","foldl","foldl1","foldr","foldr1","fromDouble","fromEnum","fromInt","fromInteger","fromIntegral","
		fromRational","fst","gcd","getChar","getContents","getLine","head","id","inRange","index","init","intToDigit","
		interact","ioError","isAlpha","isAlphaNum","isAscii","isControl","isDenormalized","isDigit","isHexDigit","
		isIEEE","isInfinite","isLower","isNaN","isNegativeZero","isOctDigit","isPrint","isSpace","isUpper","iterate","
		last","lcm","length","lex","lexDigits","lexLitChar","lines","log","logBase","lookup","map","mapM","mapM_","max","
		maxBound","maximum","maybe","min","minBound","minimum","mod","negate","not","notElem","null","numerator","odd","
		or","ord","otherwise","pi","pred","primExitWith","print","product","properFraction","putChar","putStr","putStrLn","quot","
		quotRem","range","rangeSize","read","readDec","readFile","readFloat","readHex","readIO","readInt","readList","readLitChar","
		readLn","readOct","readParen","readSigned","reads","readsPrec","realToFrac","recip","rem","repeat","replicate","return","
		reverse","round","scaleFloat","scanl","scanl1","scanr","scanr1","seq","sequence","sequence_","show","showChar","showInt","
		showList","showLitChar","showParen","showSigned","showString","shows","showsPrec","significand","signum","sin","
		sinh","snd","span","splitAt","sqrt","subtract","succ","sum","tail","take","takeWhile","tan","tanh","threadToIOResult","toEnum","
		toInt","toInteger","toLower","toRational","toUpper","truncate","uncurry","undefined","unlines","until","unwords","unzip","
		unzip3","userError","words","writeFile","zip","zip3","zipWith","zipWith3","listArray","doParse","Bool","Char","Double","Either","
    Float","IO","Integer","Int","Maybe","Ordering","Rational","Ratio","ReadS","ShowS","String","quot","rem","div","mod","elem","notElem","seq","
    EQ","False","GT","Just","LT","Left","Nothing","Right","True","Show","Eq","Ord","Num", "Word8","InPacket");
	usort($keys,'sortByLength');
  foreach($keys as $key){
  
    $pattern = '/([^{|\w|\d])('.$key.')([^\w|\d])/';
  	 $text = preg_replace($pattern,'\\1\textcolor{hgreen}{\textbf{\2}}\3',$text);
  }
  
  $keys = array("case","class","data","deriving","do","else","if","import","in","infixl","infixr","instance","let","
		module","of","primitive","then","type","where");
	usort($keys,'sortByLength');
  foreach($keys as $key){
  
    $pattern = '/([^{|\w|\d])('.$key.')([^\w|\d])/';
  	 $text = preg_replace($pattern,'\\1\textcolor{hpink}{\textbf{\2}}\3',$text);
  }
  
  $text = str_replace("\\(","\\\\(",$text);
  return $text; 
}  

function sortByLength($a,$b){
  if($a == $b) return 0;
  return (strlen($a) > strlen($b) ? -1 : 1);
}

 
