This is usage documentation, high-level documentation is at [101docs](https://github.com/101companies/101docs/tree/master/worker). It also has the [installation instructions](https://github.com/101companies/101docs/blob/master/worker/Setup.md) to start using or developing on 101worker. You further should read about the  [101meta] (https://github.com/101companies/101docs/blob/master/101meta/README.md) language.
If you dig further into the directory tree of the worker you will also find more specific readMe files for a subset.

# Structure

These are the top-level folder in the 101worker repository.

## extrators

Cotains extractors for the fact extraction in sources from different language.

## validators

Cotains validators for the validation if a file is really of the suggested language. 

## predicates

Cotains predicates that can be executed by the predicate constraint of a metaL rule.

## modules

Modules that can be executed as part of a 101worker cycle. One level of folders and one module per folder. Don't go nesting them.

See also the [section about Module Contracts](#Module-Contracts).

## libraries

Internal-use libraries. This folder will be added to the `$PYTHONPATH`, so you can just `import` them in modules written in Python. The same could be done for other languages, but right now we ain't needing it.

## configs

Contains configuration files for different 101worker cycle. The `production.json` is what's used normally.

The [test folder](configs/test) contains test configurations for [101test](https://github.com/101companies/101test).

The [env folder](configs/env) contains environment variable definitions. Those have their own [README](configs/env/README.md).

## schemas

JSON schema central.

## services

Web services relating to 101worker.

## attic

Stuff that nobody needs anymore, but you don't quite want to throw it away.

Somebody should probably clear out the attic sometime, since Git has a history of all files anyway. Unless Martin breaks it again, that is.


# Module Contracts

Modules go into the [modules folder](modules). A module consists of the following (optional things are marked as such, everything else is *required*).

* **The module itself**, which may be written in any language. Most of them are in Python though, so unless a different language is plain better at what you're trying to do, you should use Python.

* **Unit tests**. These are not optional. Currently, all tests use the [Test Anything Protocol](http://testanything.org/producers.html) and are run using `prove`. For tests in Python, see for example the [meta101 library](libraries/meta101), specifically its [Makefile](libraries/meta101/Makefile) and its [t folder](libraries/meta101/t) that contains the tests.

* **Functional tests** with [101test](https://github.com/101companies/101test). These are a bit more *optional* than unit tests, but you should still have them.

* **module.json** specifying which command is to be run, if you want your module to be incremental, which environment variables you need and which other modules depend on it. See also [the schema](schemas/module.schema.json) and [this module.json](modules/predicates101meta/module.json) as an example.

* **README.md**, with a short explanation of what it does and how to use it.

* **Documentation** with a detailed explanation of the module's purpose on [101docs](https://github.com/101companies/101docs).

* **Technical documentation**, but this is *optional* if your module is trivial. Once you have multiple files though, you should probably document your modules, functions, classes etc.

* **Makefile** with the following targets:

    * **install** (*optional*), if you need anything that doesn't come with a normal Ubuntu Server installation. These will automatically be discovered by [./install](install) and ***THEY WILL BE RUN WITH SUDO*** when 101worker is deployed. Don't go doing anything other than installs in this target. If you need to build your module, use the **build** target.

    * **build** (*optional*), if you need to compile something in your module. These targets will automatically be discovered by [./install --build](install). Everything you installed in your **install** target will be available here. This will be executed before every 101worker run, so use `make` properly and don't unecessarily re-build your stuff every time.

    * **test**, so that your tests can automatically be discovered when you run [./test](test). Everything from **install** and **build** is available here. This command *must* exit with a non-zero exit code if your tests fail.

See [pull101repo](modules/pull101repo) as an example. Pretty much all other modules are legacy and don't properly fulfill those requirements though. Don't take them as examples.

If your module derives resources, also have a look at the [meta101 library](libraries/meta101), which provides the interface for doing that. The API is documented and has examples for you.

There are also a few guidelines you must adhere to when writing your module. Any and all offences *will* lead to hard to debug issues when your module suddenly starts doing funky things and everyone will get mad at you when they found out what you did.

* Use [environment variables](configs/env) instead of hard-coding paths or URLs.

* Check if your module's files [have changed](libraries/meta101/__init__.py#L42) if you're using [meta101](libraries/meta101), so that if your module changes, the old data gets re-derived. See [predicates101meta](modules/predicates101meta/program.py) for an example.


# Cycles

In each 101worker cycle, it validates and then executes a list of modules. See the [module list used in production](configs/production.json).

The idea is that a cronjob performs these commands regularly. Just don't make it run 60 times at once, experience has shown that it don't work too well.

101worker updates itself with `git pull` after each run, so any changes in this repository will be applied in due time.

To start a cycle of 101worker, you use the [top-level Makefile](Makefile) and its `%.run` rule. For example, to run the production configuration, you'd use `make production.run`. The logs will go into the `101logs` folder, it will not output anything interesting on your terminal.

To get all output to your terminal (which you probably don't, because some modules are very noisy), you can use the `%.debug` rule instead. To run the production configuration that way, you'd you `make production.debug`.


## Run Only Select Module

If you only want to run a single module out of a configuration, you can use the `RUNONLY` environment variable and set it to the name of the module you want to run.

For example, to run only the [integrate module](modules/integrate) of the production configuration, you'd use `RUNONLY=integrate make production.debug`.


## Run Environment With Different Module Configuration

If you want to use an existing environment file , but run it with a different set of modules, you can use the `RUNCONFIG` environment variable and set it to the name of the module configuration you wish to use.

For example, if you want to use the [production.yml environment](configs/env/production.yml), but instead of the [production.json](configs/production.json) you want to use [onto.json](configs/onto.json), you simply run `RUNCONFIG=onto make production.debug`.

Note that you cannot run [pull101repo](modules/pull101repo) using `RUNCONFIG`, as this would break bookkeeping: the incrementality diff would get lost and modules wouldn't get a chance to derive new data and delete resources depending on removed primary resources.

Using both `RUNONLY` and `RUNCONFIG` behaves as you'd expect: the new configuration given by `RUNCONFIG` is used and only the module specified by `RUNONLY` is run from that configuration.
