import os

from warnings import warn
warn("const101.py is DEPRECATED, see 101worker/configs/env instead")


url101wiki          = os.environ["wiki101url"]
url101explorer      = os.environ["explorer101url"]
url101repo          = os.environ["repo101url"]
url101data          = os.environ["data101url"]
url101endpoint      = os.environ["endpoint101url"]

results101          = os.environ["results101dir"]
sRoot               = os.environ["repo101dir"]
tRoot               = os.environ["targets101dir"]
dumps               = os.environ["dumps101dir"]
views               = os.environ["views101dir"]

rulesDump           = os.environ["rules101dump"]
matchesDump         = os.environ["matches101dump"]
predicatesDump      = os.environ["predicates101dump"]
fragmentsDump       = os.environ["fragments101dump"]
geshiDump           = os.environ["geshi101dump"]
validatorDump       = os.environ["validator101dump"]
extractorDump       = os.environ["extractor101dump"]
metricsDump         = os.environ["metrics101dump"]
fragmentMetricsDump = os.environ["fragmentMetrics101dump"]
summaryDump         = os.environ["summary101dump"]
suffixesDump        = os.environ["suffixes101dump"]
importsDump         = os.environ["imports101dump"]
resolutionDump      = os.environ["resolution101dump"]
wikiDump            = os.environ["wiki101dump"]
pullRepoDump        = os.environ["pullRepo101dump"]
moduleSummaryDump   = os.environ["moduleSummary101dump"]
tModuleSummaryDump  = os.environ["moduleSummary101temp"]


def noMetrics():
    result = dict()
    result["size"] = 0
    result["loc"] = 0
    result["ncloc"] = 0
    return result
