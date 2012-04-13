#!/bin/sh
echo Performing module $1
cd modules/$1; make
