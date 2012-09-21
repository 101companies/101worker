#! /usr/bin/env python

import os
import sys
import urllib
import zipfile
sys.path.append('../../libraries/101meta')
import const101

def progress(blockCount, blockSize, totalSize):
	status = r"%10d  [%3.2f%%]" % (blockCount*blockSize, blockCount*blockSize * 100. / totalSize)
	status = status + chr(8)*(len(status)+1)
	print status,


url = "http://data.101companies.org/zips/";

#retrieve data
print "downloading dumps"
urllib.urlretrieve(url+"dumps.zip", "./dumps.zip", progress)
print "\ndownloading resources"
urllib.urlretrieve(url+"resources.zip", "./resources.zip", progress)
print "\ndownloading 101repo"
urllib.urlretrieve(url+"101repo.zip", "./101repo.zip", progress)

print "\nextracting dumps"
#extract dumps
f = zipfile.ZipFile("./dumps.zip", "r")
f.extractall(const101.dumps)

print "extracting resources"
#extract resources
f = zipfile.ZipFile("./resources.zip", "r")
f.extractall(const101.tRoot)

print "extracting 101repo"
f = zipfile.ZipFile("./101repo.zip", "r")
f.extractall(const101.sRoot)

print "cleaning up"
os.remove("./dumps.zip")
os.remove("./resources.zip")
os.remove("./101repo.zip")
