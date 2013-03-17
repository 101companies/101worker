import sys
import json
import checker

contribNames = sorted(json.loads(file(sys.argv[1]).read())['dirs'])
#print checker.check("html5tree")
for contribName in contribNames:
	print "Checking " + contribName + " ..."
	report = checker.check(contribName)
	with open(sys.argv[2] + contribName + '.json', 'w+') as reportf:
		json.dump(report, reportf)
	with open(sys.argv[2] + contribName + '.jsonp', 'w+') as reportpf:
		reportpf.write("callback(")
		reportpf.write(json.dumps(report))
		reportpf.write(")")


