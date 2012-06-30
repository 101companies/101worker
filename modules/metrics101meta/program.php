<?php
define('_MEGALIB','true');
define('DEBUG',10);
define('ABSPATH_BASE',dirname(dirname(dirname(__DIR__))).'/');
define('ABSPATH_EXTERNAL_LIBRARIES',ABSPATH_BASE.'101results/libraries/');
define('ABSPATH_MEGALIB',ABSPATH_EXTERNAL_LIBRARIES.'megalib/');
define('ABSPATH_SRC_GESHI_LIBRARY',ABSPATH_EXTERNAL_LIBRARIES.'geshi/');
require_once ABSPATH_MEGALIB.'SourceCode.php';
$foo = new GeSHiExtended('foo','text');
echo $foo->getNLOC();
?>