#!/bin/sh

if python --version >/dev/null 2>&1; then
    echo "Python is installed"
else
    echo "Please install Python"
    exit
fi

if ghc --version >/dev/null 2>&1; then
    echo "Haskell is installed"
else
    echo "Please install Haskell"
    exit
fi
if node --version >/dev/null 2>&1; then
    echo NodeJs is installed
else
    echo "Please install NodeJs"
    exit
fi
if java -version >/dev/null 2>&1; then
    echo "Java is installed"
else
    echo "Please install Java"
    exit
fi

if mono --version >/dev/null 2>&1; then
    echo "Mono is installed"
else
    echo "Please install Mono"
    exit
fi



echo "Everything is installed properly. I will check now if the module dependencies are all there as well"

if python -c 'import sqlparse' >/dev/null 2>&1; then
    echo "The sqlparse module is installed"
else
    echo "Trying to install module"
    if pip --version >/dev/null 2>&1; then
        pip install sqlparse
    else
        echo "Please install pip or the module Sqlparse without a packadge manager"
        exit
    fi
fi

if cabal --version >/dev/null 2>&1; then
    read -p "Shall we install Json Modul for haskell? Type Y is so " input
    if [ "$input" = "Y" ]; then
        cabal install json
    fi
else
    echo "Please install cabal or through another way the modul 'json'"
fi

if npm -v >/dev/null 2>&1; then
    if npm version esprima >/dev/null 2>&1; then
        echo "Esprima is installed"
    else
        echo "Trying to install or update Esprima"
        npm install esprima
    fi

else
    echo "Please install NPM'"
fi



read -p "The environment should be set up now. Shall we run the test cases now? Y for yes: " input
if [ "$input" = "Y" ]; then
    sh testExtractors.sh
fi


