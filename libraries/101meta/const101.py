import os

sRoot = "../../../101results/101repo" # the root for source files
tRoot = "../../../101web" # the root for target files
dumps = os.path.join(tRoot, "dumps")
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

def noMetrics():
    result = dict()
    result["size"] = 0
    result["loc"] = 0
    result["ncloc"] = 0
    return result
