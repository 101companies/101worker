Adding a module

Go to "101worker/modules".
Edit "production.config".
That is, add the module in question.
This could be done on any machine with a clone.
The worker machine will pick up the change from git.
That is, the machine pulls changes at the end of each cycle.


Execution of a cycle

Go to "101worker".
Run "make".
Module results are temporarily to be stored in ../101temps.
Module results are eventually to be stored in ../101results.
Module arguments are to be fetched from ../101results.
A log of the latest cycle is stored in ../101logs/runner.log.
The log is sent via email, if any module failed.


Testing

See modules/test* for typical scenarios of modules.
Run "make testOk.reconfigure" to prepare for positive tests.
Run "make testFail.reconfigure" to prepare for negative tests.
Run "make" to exercise tests.
Run "make production.reconfigure" to return to production.
