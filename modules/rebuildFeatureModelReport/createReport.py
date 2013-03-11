import sys
import json
import checker

contribNames = sorted(json.loads(file(sys.argv[1]).read())['dirs'])
#print checker.check("html5tree")
report = {}
for contribName in contribNames:
	print "Checking " + contribName + " ..."
	report[contribName] = checker.check(contribName)
with open(sys.argv[2], 'w+') as reportf:
  json.dump(report, reportf)
