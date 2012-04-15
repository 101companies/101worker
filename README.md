# The notion of module

101worker components of execution are called modules.

All modules are located in "101worker/modules".

See "101worker/modules/test*" for illustrative modules.

A module <x> can be executed as follows:

* Change directory to "101worker".
* Enter "make <x>.run".

This mode of execution is good for testing.

See the "test" target of "101worker/Makefile" for illustration.

Modules would be added to the production list at some point; see below.

Modules should access the file system as follows:

* Module results are temporarily to be stored in "../101temps".
* Module results are eventually to be stored in "../101results".
* Module arguments are to be fetched from "../101results".

All the mentioned directories are automatically created, if needed.


# Production cycle by 101worker

101worker repeatedly executions a certain list of modules.

See the file "101worker/configs/production.config" for the list.

Module names are to be separated by spaces.

The production cycle can be manually invoked as follows:

* Change directory to "101worker".
* Enter "make".

The idea is that a cron job performs these commands regularly.

101worker updates itself by "git pull" before each run.

In this manner, production modules can also be added remotely.

A log of the latest cycle is stored in "../101logs/runner.log".

The log is sent via email to the 101gatekeepers, if any module failed.


Alternative module lists

The default list is "101worker/configs/production.config".

Alternative module lists may be good for testing 101worker.

A list <x> can be selected as follows:

* Change directory to "101worker".
* Enter "make <x>.reconfigure".

At the time of writing, these module lists <x> exist:

* "testOk": positive tests.
* "testFail": negative tests.
* "production": production.


# TODO

NONE
