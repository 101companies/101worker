meta101
=======

This is a rewrite of the old [101meta library](../101meta), with a cleaner
interface, tests and documentation. The old library is deprecated, don't use
it anymore.

See [the main module file](__init__.py) for documentation and examples showing
you how to use this library. If you have pydoc installed, you can also just run
`make` and it'll show you the documentation.


Installation
------------

Just run `sudo make install` to install dependencies needed for testing. Even
better, run [./install](../../install) in this repository's root to install all
dependencies of 101worker.


Testing
-------

After installing testing requirements, run `make test`. You can also run
`make cover` to get code coverage information. You may also run
[./test](../../test) in this repository's root to run all tests of 101worker.
