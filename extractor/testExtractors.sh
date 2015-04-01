#!/bin/sh

#Easy Bash Script that executes all the test case of the extractors who have a test-case and finally prints the result


red='\033[0;31m'
NC='\033[0m' # No Color

function checkTestSuccess {
    if make run-test > /dev/null 2>&1 ; then
        echo $1 "extractor seems to work"
    else
        echo "${red} Error in the extractor for" $1 " ${NC}"
    fi
}

cd HTML/
checkTestSuccess HTML
cd ..

cd Haskell/
checkTestSuccess Haskell
cd ..


cd JSON/
checkTestSuccess JSON
cd ..

cd JavaScript/
checkTestSuccess JavaScript
cd ..

cd JAVA/
checkTestSuccess JAVA
cd ..

cd Python/
checkTestSuccess Python
cd ..

cd SQL/
checkTestSuccess SQL
cd ..

cd XMI/
checkTestSuccess XMI
cd ..

cd XSD/
checkTestSuccess XSD
cd ..
