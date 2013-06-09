import os

url101wiki = "http://101companies.org/index.php/"
url101repo = "https://github.com/101companies/101repo/tree/master/"
results101 = "../../../101results"
sRoot = "../../../101results/101repo" # the root for source files
tRoot = "../../../101web/data/resources" # the root for target files
dumps = "../../../101web/data/dumps" # the root for dumps
views = "../../../101web/data/views" # the root for views
rulesDump = os.path.join(dumps, "rules.json")
matchesDump = os.path.join(dumps, "matches.json")
predicatesDump = os.path.join(dumps, "predicates.json")
fragmentsDump = os.path.join(dumps, "fragments.json")
geshiDump = os.path.join(dumps, "geshi.json")
validatorDump = os.path.join(dumps, "validator.json")
extractorDump = os.path.join(dumps, "extractor.json")
metricsDump = os.path.join(dumps, "metrics.json")
summaryDump = os.path.join(dumps, "summary.json")
suffixesDump = os.path.join(dumps, "suffixes.json")
importsDump = os.path.join(dumps, "imports.json")
resolutionDump = os.path.join(dumps, "resolution.json")
wikiDump = os.path.join(dumps, "wiki.json")
pullRepoDump = os.path.join(dumps, "PullRepo.json")
moduleSummaryDump = os.path.join(dumps, 'ModuleSummaryDump.json')

def noMetrics():
    result = dict()
    result["size"] = 0
    result["loc"] = 0
    result["ncloc"] = 0
    return result
