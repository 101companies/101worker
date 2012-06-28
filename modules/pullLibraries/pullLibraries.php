<?php
$n=0 ;
$thisScript=$argv[$n++];
$librariesConfigFile=$argv[$n++];
$workerTimeLibrariesDir=$argv[$n++];
$webTimeLibrariesDir=$argv[$n++];
$baseDirectory=$argv[$n++];

echo "Starting pullLibraries\n" ;
echo "  config file     = ".checkExist($librariesConfigFile)."\n" ;
echo "  workerTime dir  = ".checkExist($workerTimeLibrariesDir)."\n" ;
echo "  webTime dir     = ".checkExist($webTimeLibrariesDir)."\n" ;;
echo "  base dir        = ".checkExist($baseDirectory)."\n" ;

$libraries = readLibraryDefinitions($librariesConfigFile) ;
foreach($libraries as $libraryName => $info ) {
  processLibraryDeclaration($libraryName,$info,$baseDirectory,$workerTimeLibrariesDir,$webTimeLibrariesDir) ;
}









function readLibraryDefinitions($librariesConfigFile) {
  $jsonString=file_get_contents($librariesConfigFile) ;
  if ($jsonString===false) {
    echo("$thisScript: file $librariesConfigFile not found\n") ;
    exit(2) ;
  }
  $libraries = json_decode($jsonString,true) ;
  if ($libraries===null) {
    echo("$thisScript: error in json file $librariesConfigFile\n" ) ;
    exit(3) ;
  }
  return $libraries ;
}

function checkExist($file) {
  if (@ file_exists($file)) {
    return $file." : FOUND" ;
  } else {
    echo $file." : NOT FOUND!!!\n" ;
    exit(4) ;
  }
}


function processLibraryDeclaration($libraryName,$info,$baseDirectory,$workerTimeLibrariesDir,$webTimeLibrariesDir) {
  if (isset($info['workertime']) && $info['workertime']==='yes') {
    pullLibrary($libraryName,$info,$baseDirectory,$workerTimeLibrariesDir.'/'.$libraryName) ;
  } ;
  if (isset($info['webtime']) && $info['webtime']==='yes') {
    pullLibrary($libraryName,$info,$baseDirectory,$webTimeLibrariesDir.'/'.$libraryName) ;
  } ;  
}

function pullLibrary($libraryName,$info,$baseDirectory,$targetDirectory) {
  if ($info["updates"]==="onlyOnce" && is_dir($targetDirectory)) {
    echo "---------------------------------------------------------------------\n" ;
    echo "library $libraryName is already in $targetDirectory => no updates\n" ;   
    echo "---------------------------------------------------------------------\n"  ;
    echo "The update mode is declared as ".$info["updates"]." in the configuration file\n" ;
    echo "so this library is created but not updated. You can still remove the existing one\n" ;
    echo "or change the configuration file if needed" ;
    return ;
  }
  createDir($targetDirectory) ;
  echo "\n" ;
  echo "----------------------------------------------------------------\n" ;
  echo "pulling library '$libraryName' to $targetDirectory\n" ;
  echo "----------------------------------------------------------------\n" ;
    if (isset($info['github'])) {
    pullGithub($info['github'],$targetDirectory) ;
  } elseif (isset($info['dir'])) {
    pullDirectory($baseDirectory.'/'.$info['dir'],$targetDirectory) ;
  } elseif (isset($info['urls'])) {
    foreach($info['urls'] as $url => $targetBasename) {
      pullUrl($url,$targetDirectory,$targetBasename) ;
    }
  } else {
    echo("Don't know what to do with library $libraryName. No type recognized") ;
    exit(5) ; 
  }
  echo "library $libraryName pulled\n" ;
  
}

function pullGithub($githubRepository,$targetDirectory) {
  // using pullgithub.sh is not enough as . may not be in the path
  // similarily ./pullgithub.sh is not interpreted correctly on windows
  $cmd=getcwd()."/pullgithub.sh" 
       ." ".escapeshellarg($githubRepository)
       ." ".escapeshellarg($targetDirectory)
       ." 2>&1";
  echo "executing $cmd \n";
  
  system($cmd,$exitcode) ; 
  if ($exitcode !=0) {
    echo("failed with exit code $exitcode: $cmd");
    exit(6) ;
  }
}

function pullDirectory($sourceDirectory,$targetDirectory) {
  $cmd="cp -r -v" 
       ." ".escapeshellarg($sourceDirectory.'/').'*'
       ." ".escapeshellarg($targetDirectory)
       ." 2>&1";
  system($cmd,$exitcode) ; 
  if ($exitcode !=0) {
    echo("failed with exit code $exitcode: $cmd");
    exit(7) ;
  }
}

function pullUrl($url,$targetDirectory,$targetBasename) {
  echo "  Downloading $url ..." ;
  $filecontent = file_get_contents($url) ;
  if ($filecontent===false) {
    echo("cannot load url $url") ;
    exit(8) ;
  } else {
    echo "done. ".strlen($filecontent)." bytes read.\n" ;
  }
  $targetfile=$targetDirectory.'/'.$targetBasename ;
  
  echo "    saving to ".$targetfile.' ... ' ; 
  if(file_put_contents($targetfile,$filecontent)===false) {
    echo("$thisScript: ERROR while saving");
    exit(9) ;
  }
  echo " done\n" ;
}

function createDir($directory) {
  if (! is_dir($directory)) {
    if (@ !mkdir($directory)) {
      echo("cannot create directory $directory") ;
      exit(10) ;
    }
  }
}
