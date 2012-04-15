Regular execution

Run "make" to execute all modules.
Module results are temporarily to be stored in ../101temps.
Module results are eventually to be stored in ../101results.
Module arguments are to be fetched from ../101results.
A log of module execution is stored in ../101logs/runner.log.


Testing

See modules/test* for typical scenarios of modules.
Run "make testOk.reconfigure" to prepare for positive tests.
Run "make testFaik.reconfigure" to prepare for negative tests.
Run "make" to to exercise positive and negative tests.
Run "make production.reconfigure" to return to production.
An email is send in the case of failing modules.
That is, an email is send for negative tests.


Adding a module

Go to modules.
Edit production.config.
That is, add the module in question.
Regular execution will automatically pick up the change.
