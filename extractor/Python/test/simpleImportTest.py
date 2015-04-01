import os
import sys

for root, dirs, files in os.walk(repo101dir, followlinks=True):
	print files
	
import json