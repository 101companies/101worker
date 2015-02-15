# Structure

## modules

## libraries

## configs

## schemas

## services

## attic

# Module Contracts

TODO

All the mentioned directories are automatically created, if needed.


# Production cycle by 101worker

101worker repeatedly executes a certain list of modules.

See the file `101worker/configs/production.json` for the list.

Module names are stored in a json list.

The production cycle can be manually invoked as follows:

* Change directory to `101worker`.
* Enter `make`.

The idea is that a cron job performs these commands regularly.

101worker updates itself with "git pull" after each run.

In this manner, production modules can also be added remotely.

TODO talk about logging.


# Adding a module

TODO


# Alternative module lists

The default list is `101worker/configs/production.json`.

TODO talk about env, testing in 101test


# TODO

* this documentation

* unit tests of meta101, runner, pull101repo

* documentation of meta101

* handling of module failure, saving its diff

* incrementalization of modules:

Module                      | Status
----------------------------|:--------:
pull101repo                 | ok
pull                        | n/a
pullLibraries               | n/a
build                       | n/a
gatherGeshi                 | n/a
rules101meta                | ok
matches101meta              | ok
geshi101meta                | ok
metrics101meta              | ok
validate101meta             | ok
extract101meta              | ok
fragmentMetrics101meta      | ok
refineTokens                | **not ok**
predicates101meta           | ok
fragments101meta            | ok
summary101meta              | **not ok**
imports101meta              | **not ok**
wiki2json                   | **not ok**
themesExtractor             | **not ok**
languageExtractor           | **not ok**
vocabulary                  | **not ok**
wiki2tagclouds              | **not ok**
moretagclouds               | **not ok**
members                     | **not ok**
summarizeModuleDescriptions | **not ok**
resolve101meta              | **not ok**
index101meta                | **not ok**
repo2charts                 | **not ok**
wiki101JsonToWiki101RDF     | **not ok**
loadWiki101RDF              | **not ok**
parseMegaL                  | **not ok**
webDeployMegaModels         | **not ok**
rebuildXmlCatTree           | **not ok**
validateModuleDescriptions  | **not ok**
zip                         | **not ok**
extractClaferFeatureModel   | **not ok**
integrate                   | **not ok**
