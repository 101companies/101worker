#!/usr/bin/python
import sys
import json

i = sys.argv[1]

f = open(i, 'r')
lines = [i.strip() for i in f.readlines()]

print json.dumps(lines)


