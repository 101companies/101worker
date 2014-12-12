pull101Repo
===========

101worker module for getting the latest 101repo and all its dependent repos
from GitHub. It also gathers a diff off all the files changed since it was
last run.

Architecture
------------

This module is written in Perl. `pull101repo` is the main script that will pull
101repo in production mode.

The folder `Repo101` contains two Perl modules with the actual functionality
and their documentation in POD at the bottom. This documentation is replicated
in markdown in the `doc` folder.

Tests can be found in the `t` folder and can be run using `prove`. If a bug is
found in this module, a test case to replicate the error should be created
before the bug fix is attempted.

Installation
------------

If you are running on a Linux with apt-get, perl and cpan installed (any Ubuntu-
or Debian-like Linux should have those), just run `sudo make install`.

Otherwise, you need a moderately recent perl and install the CPAN modules that
you see in the Makefile.

Testing
-------

Run `make test` to run the test suite using `prove`. You can also run
`make cover` to build code coverage information using `cover` into the folder
`cover_db`.

Running
-------

Make sure that `make test` runs successfully first. Then just type `make run`.

This can also be run as a job in 101worker, and probably should be run before
any other modules, since without 101repo you can't do too much.
