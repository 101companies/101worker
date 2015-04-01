#!/bin/sh

#Easy Bash Script that executes all the test case of the extractors who have a test-case and finally prints the result
#ToDo: Make it dynamic and not static...hence check out all folders and execute make

red='\033[0;31m'
NC='\033[0m' # No Color

function checkTestSuccess {
    if make test > /dev/null 2>&1 ; then
        echo $1 "Validator seems to work"
    else
        echo "${red} Error in the extractor for" $1 " ${NC}"
    fi
}

cd CSharpValidator/
checkTestSuccess CSharpValidator
cd ..

cd JValidator/
checkTestSuccess JValidator
cd ..


cd XSDValidator/
checkTestSuccess XSDValidator
cd ..

cd JTidyValidator/
checkTestSuccess JTidyValidator
cd ..

cd W3CValidator/
checkTestSuccess W3CValidator
cd ..


