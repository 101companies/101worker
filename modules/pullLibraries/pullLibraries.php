<?php
$n=0 ;
$thisScript=$argv[$n++];
$librariesConfigFile=$argv[$n++];
$workerTimeLibrariesDir=$argv[$n++];
$webTimeLibrariesDir=$argv[$n++];
$baseDirectory=$argv[$n++];

echo "Starting pullLibraries\n" ;
echo "  config file     = $librariesConfigFile\n" ;
echo "  workerTime dir  = $workerTimeLibrariesDir\n" ;
echo "  webTime dir     = $webTimeLibrariesDir\n" ;
echo "  base dir        = $baseDirectory\n" ;

$jsonString=file_get_contents($librariesConfigFile) ;
if ($jsonString===false) {
  die("$thisScript: file $librariesConfigFile not found") ;
}
$libraries = json_decode($jsonString,true) ;
if (isset($libraries)===null) {
  die("$thisScript: error in json file $librariesConfigFile" ) ;
}
foreach($libraries as $libraryName => $info ) {
  processLibraryDeclaration($libraryName,$info) ;
}


function processLibraryDeclaration($libraryName,$info) {
  global $workerTimeLibrariesDir ;
  global $webTimeLibrariesDir ;
  if (isset($info['workertime']) && $info['workertime']==='yes') {
    pullLibrary($libraryName,$info,$workerTimeLibrariesDir.'/'.$libraryName) ;
  } ;
  if (isset($info['webtime']) && $info['webtime']==='yes') {
    pullLibrary($libraryName,$info,$webTimeLibrariesDir.'/'.$libraryName) ;
  } ;  
}

function pullLibrary($libraryName,$info,$targetDirectory) {
  global $thisScript ;
  global $baseDirectory ;
  createDir($targetDirectory) ;
  echo "pulling library '$libraryName' from " ;
  if (isset($info['github'])) {
    echo "github ".$info['github']."\n" ;
    pullGithub($info['github'],$targetDirectory) ;
  } elseif (isset($info['dir'])) {
    echo "directory ".$info['dir']."\n" ;
    pullDirectory($baseDirectory.'/'.$info['dir'],$targetDirectory) ;
  } elseif (isset($info['urls'])) {
    foreach($info['urls'] as $url) {
      echo "url ".$url.' ... ' ;
      pullUrl($url,$targetDirectory) ;
    }
  } else {
    die("$thisScript: don't know what to do with library $libraryName. No type recognized") ;
  }
  echo "done\n" ;
  
}

function pullGithub($githubRepository,$targetDirectory) {
  global $thisScript ;
  $cmd=getcwd()."/pullgithub.sh" 
       ." ".escapeshellarg($githubRepository)
       ." ".escapeshellarg($targetDirectory)." ";
  $output="" ;
  if (system($cmd,$exitcode)===false) {
    die("$thisScript: failed: $cmd");
  }
}

function pullDirectory($sourceDirectory,$targetDirectory) {
  global $thisScript ;
  $cmd="cp -r -v " 
       ." ".escapeshellarg($sourceDirectory.'/').'*'
       ." ".escapeshellarg($targetDirectory) ;
  if (system($cmd,$exitcode)==false) {
    die("$thisScript: failed: $cmd");
  }
}

function pullUrl($url,$targetDirectory) {
  global $thisScript ;
  $filecontent = file_get_contents($url) ;
  if ($filecontent===false) {
    die("$thisScript: cannot load url $url") ;
  }
  $targetfile=$targetDirectory.'/'.basename($url) ;
  if(file_put_contents(basename($url),$filecontent)===false) {
    die("$thisScript: cannot save url $url to file $targetfile");
  }
}

function createDir($directory) {
  global $thisScript ;
  if (! is_dir($directory)) {
    if (@ !mkdir($directory)) {
      die("$thisScript: cannot create directory $directory") ;
    }
  }
}
