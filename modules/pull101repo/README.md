pull101Repo
===========

101worker module for getting the latest 101repo and all its dependent repos
from GitHub. It also gathers a diff off all the files changed since it was
last run.

Installation
------------

If you are running on a Linux with apt-get, perl and cpan installed (any Ubuntu-
or Debian-like Linux should have those), just run `sudo make install`.

Otherwise, you need a moderately recent perl and install the CPAN modules that
you see in the Makefile.

After installing, run `make test` to see if everything works fine.

Running
-------

Make sure that `make test` runs successfully first. Then just type `make run`.

This can also be run as a job in 101worker, and probably should be run before
any other modules, since without 101repo you can't do too much.
