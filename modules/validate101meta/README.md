# Headline

A module to validate files in the 101repo

# Input

* 101results/101repo via module pull101repo
* 101web/dumps/rules.json via module rules101meta
* 101web/dumps/matches.json via module match101meta

# Output

[dumps/validator.json](http://black42.uni-koblenz.de/production/101worker/dumps/validator.json)

# Description

Validators are assigned to files with the "validator" key of 101meta metadata. Validation is performed incrementally by the module such that only new files or modified files are validated (when compared to the previous run of the module). The dump contains the following data:

* numbers
** numberOfFiles: files with assigned validator
** numberOfSuccesses: successful validations 
** numberOfFailures: successful validations 
** numberOfInserts: validations added since previous run 
** numberOfUpdates: validations re-performed since previous run 
* validators: the filenames of all validators encountered
* problems: logging data of failed validator executions or validator executions

# Methodology

Ideally, _all_ files are validated and _all_ validations succeed. Realistically, validators may not be readily available for all files, but more validators can be added over time. Also, validations may fail for various reasons: incorrect association between file and validator, incorrect validator, too strict validator, invalid file. The goal shall be to eliminate failing validations by changing files, changing validators, adding validators, or changing associations between files and validators.
