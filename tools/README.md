101worker Tools
===============

Contains various tools used during the execution of a 101worker cycle.

All tools except the runner will assume that they are being called from the 101worker root directory and that they're dealing with a production run, i.e. that all output goes into the directory above the 101worker root directory.

This means that they won't work for test cases, but that's because they're not meant for that. It's pointless to archive or report on or build a dependency graph over a test case.

What follows is a short documentation about each of the tools, how they are to be executed and by which targets in the [101worker Makefile](../Makefile) they are called.


runner
------

    tools/runner/runner < configs/env/production.yml

Loads the environment variables from the YAML file given on its stdin, validates that everything is sane and then runs the modules specified by the `config101` environment variable. Also handles all of the diff in- and output for each module. See `runner/doc` for detailed module documentation.

This is run by `make %.run`, `make %.debug`, `make %.depend` and the tests in the [101test repo](https://github.com/101companies/101test).


loadenv
-------

    tools/loadenv configs/env/production.yml

Loads the environment variables form the given YAML file and dumps it as JSON.

See also [the runner README](runner/README.md).


archiver
--------

    tools/archiver

Archives the last logs from `101logs` into `101web/$currentTime` so that they're visible at http://worker.101companies.org/logs/. Also writes that current time to `101web/lastArchive`.

This is run by `make archive`.


reporter
--------

    tools/reporter

Produces a nice and colorful HTML report from the last `runner.log`. This report is saved as `101web/$lastArchive/report.html` and sent to the 101gatekeepers via e-mail.

Note that this e-mail report currently only works in the University of Koblenz network. Also note that if you run this on your own computer in that network, you will cause a real report to be sent.

This is run by `make report`.


depend
------

    tools/depend CHANGESFILE...

Produces a Graphviz graph from the given CHANGESFILEs, which can be created by the runner.

This is run by `make depend`, look there for how the runner can be coerced into creating those CHANGESFILEs.
