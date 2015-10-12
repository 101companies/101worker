<?php

require_once(BASE_PATH . '../libraries/MediaWikiAPI/Utils.php');

function formatTex(){
 $fileName = BASE_PATH . "wiki2tex/tex/content/data/macros_raw.tex";
 $file_array = file($fileName, FILE_IGNORE_NEW_LINES);
 $fOutput = fopen("tex/content/data/macros.tex", "w+");
 //var_dump($file_array);
 foreach ($file_array as $line)
 {
   if(startsWith("\\item \\wikiref", $line)){
     $line = formatter::toTex($line);
  }
  else{
    $line = formatter::toTex($line);
  }
  fwrite($fOutput, $line . PHP_EOL);
 }

 fclose($fOutput);
}
?>
