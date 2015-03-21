pull101Repo
===========

This is usage documentation. Refer to [101docs](https://github.com/101companies/101docs/blob/master/worker/modules/pull101repo.md) for high-level documentation.


Architecture
------------

This module is written in Perl. `pull101repo` is the main script that will pull 101repo in production mode.

The folder `Repo101` contains two Perl modules with the actual functionality and their documentation in POD at the bottom. This documentation is replicated in markdown in the `doc` folder.

Tests can be found in the `t` folder and can be run using `prove`. If a bug is found in this module, a test case to replicate the error should be created before the bug fix is attempted.


Installation
------------

Just run `sudo make install` and you should be ready to go. Even better would be if you ran the [install script](../../install) in the 101worker root directory to install all dependencies of modules, libraries and tools.


Testing
-------

Just run `make test`, or even better run the [test script](../../test) in the 101worker root directory to run all available tests.

If you want to get developer tests, first run `export TEST101DEVEL=1` and then run `make test`. Please read [the note about atime](doc/Runner101::Changes.md) first, otherwise you can get failing tests.

To get the documentation coverage test to run, you also need to run `cpan Test::Pod::Coverage`, otherwise the test will just be skipped.

If you want to get test coverage, run `make cover`. This requires `cpan Devel::Cover`. You should have `TEST101DEVEL` enabled for this, otherwise some code that's not relevant to production won't get tested.


101test
-------

There is a magical environment variable called `repo101branch`. If this variable is set, the branch given in it will be checked out for whatever is pulled as 101repo.

This is used in [101test](https://github.com/101companies/101test) to simulate changes in 101repo without having to actually modify a repository.


Running
-------

Make sure that `make test` runs successfully first.

Then run this as part of 101worker. It probably should be run before any other modules, since without 101repo you can't do too much.
