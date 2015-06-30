kludge101
=========

This library is a kludge to close a security hole of running random executables
from arbitrary repositories. Using this library is *deprecated*, because you're
doing something wrong if you need it. Once the security hole is closed proper
and all those executables are moved into 101worker, this library should be
deleted to prevent anyone from even trying to use it.

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
