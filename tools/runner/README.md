Runner
======

    ./runner < config.yml

Validates and runs modules. Also handles everything related to diff incrementality and logs.

See the `%.run`, `%.debug` and `%.depend` targets in the [101worker Makefile](../../Makefile) and the [101test repo](https://github.com/101companies/101test) for places where the runner is called. You can also find detailed module documentation about the runner in the [doc folder](doc).


Installation
------------

Just run `sudo make install` and you should be ready to go. Even better would be if you ran the [install script](../../install) in the 101worker root directory to install all dependencies of modules, libraries and tools.


Testing
-------

Just run `make test`, or even better run the [test script](../../test) in the 101worker root directory to run all available tests.

If you want to get developer tests, first run `export TEST101DEVEL=1` and then run `make test`. Please read [the note about atime](doc/Runner101::Changes.md) first, otherwise you can get failing tests.

To get the documentation coverage test to run, you also need to run `cpan Test::Pod::Coverage`, otherwise the test will just be skipped.

If you want to get test coverage, run `make cover`. This requires `cpan Devel::Cover`. You should have `TEST101DEVEL` enabled for this, otherwise some code that's not relevant to production won't get tested.
