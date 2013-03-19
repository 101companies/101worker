import sys
import json
import checker

def writeReport(report, pathBase):
	with open(pathBase + '.json', 'w+') as reportf:
		json.dump(report, reportf)
	with open(pathBase + '.jsonp', 'w+') as reportpf:
		reportpf.write('callback(' + json.dumps(report) + ')')

contribNames = sorted(json.loads(file(sys.argv[1]).read())['dirs'])
summary = {}
for contribName in contribNames:
	print 'Checking ' + contribName + ' ...'
	report = checker.check(contribName)
	writeReport(report, sys.argv[2] + sys.argv[3] + contribName)
	summary[contribName] = report
writeReport(summary, sys.argv[2] + 'featureModelReport')
