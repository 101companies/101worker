Environment Variable Definitions
================================

Constants for 101worker are defined in environment variables. These consist of file paths, directory paths and URLs.

File paths and directory paths are similar to each other: they are given relative to the directory that the 101worker directory is in and will be turned into absolute paths by the runner. Directory paths *must* and file paths *must not* not end with a slash, that way the runner can disambiguate between a file and a directory paths. All directories that appear in any path will be created automatically if they don't exist. Nonexistent files will *not* be created (which is why there is a need for disambiguation). However, the resulting environment variables *will never have a trailing slash*!

You can also reference other paths using `$keyname`. For example, if you want to put the file *matches.json* into the folder defined by *dumps101dir*, you'd just write `$dumps101dir/matches.json`.

There are a handful of paths that are always defined from the get-go. You can override these in your config if you really want to, but it's more useful to reference them and build further paths out of them:

* `$output101dir` - The directory where all output should go.

* `$worker101dir` - The root directory of 101worker.

* `$modules101dir` - Worker modules directory. Probably not useful here.

* `$logs101dir` - Directory where runner and module logs go to. Also not useful.

* `$diffs101dir` - Diff- and changes-related output directory of the runner. You shouldn't mess with this.

* `$last101run` - Contains a timestamp of the last 101worker run, or 0 if it hasn't been run before.

URLs are only special if they start with the `file://` scheme. In that case, their path will be turned into an absolute `file://` URL as described above. The same rule for trailing slashes apply. Other URLs like `http://` or `https://` won't be touched.

For examples, see the definition files in the folder of this README.

Intent
------

This is primarily intended to replace `libraries/101meta/const101.py`, which is just a Python module that holds a bunch of hard-coded strings, which is silly and inflexible. It also replaces the redundant definitions in `101worker/Makefile.vars` and probably various other Makefiles and hard-coded paths in modules.

The environment variable approach fulfills the “Single Point of Truth” or “Once and Only Once” rule: they are defined in one place and can be accessed from virtually any programming environment. It is also much more flexible and allows creation of a test environment.

The const101 Python module and Makefile.vars are therefore *deprecated* and will hopefully be removed soon.

Accessing Environment Variables
-------------------------------

Getting a value from an environment variable is utterly trivial in virtually any language. In shell scripts and Makefiles, you can even just reference them as if they were regular variables.

Here's examples on how to do it in the various languages used in 101worker:

### Python

```python
#!/usr/bin/env python
# os.environ is a dict with the environment
import os
repo_path = os.environ["repo101dir"]
repo_url  = os.environ["repo101url"]
```

### Perl

```perl
#!/usr/bin/perl
# %ENV is a hash with the environment
my $repo_path = $ENV{repo101dir};
my $repo_url  = $ENV{repo101url};
```

### Ruby

```ruby
#!/usr/bin/env ruby
# ENV is a hash with the environment
repo_path = ENV['repo101dir']
repo_url  = ENV['repo101url']
```

### PHP

```php
<?php
# Use the getenv function. It's case-insensitive for
# some reason, but that shouldn't break anything.
$repo_path = getenv('repo101dir');
$repo_url  = getenv('repo101url');

# There's also the superglobal array $_ENV, but don't use
# that because it doesn't work with all configurations.
```

### Bourne Shell and Friends

```sh
#!/bin/sh
ls "$repo101dir"
wget "$repo101url"
```

### Make

```make
run: ${repo101dir}
	python program.py
```

Constant Documentation
----------------------

These are the constants that are currently in use. This is a big TODO.

Name                   | Type      | Description
---------------------- | --------- | -----------------------------------------------------
config101              | File      | Module configuration file, used by runner
repo101dir             | Directory | Where 101repo gets pulled to
gitdeps101dir          | Directory | Where 101repo dependencies get pulled to
targets101dir          | Directory | 
dumps101dir            | Directory | Where dump results go
views101dir            | Directory | Where view results go
rules101dump           | File      | Location of 101meta rules dump
matches101dump         | File      | 
predicates101dump      | File      | 
fragments101dump       | File      | 
geshi101dump           | File      | 
validator101dump       | File      | 
extractor101dump       | File      | 
metrics101dump         | File      | 
fragmentMetrics101dump | File      | 
summary101dump         | File      | 
suffixes101dump        | File      | 
imports101dump         | File      | 
resolution101dump      | File      | 
wiki101dump            | File      | 
repo101url             | URL       | Remote URL for 101repo
gitdeps101url          | URL       | URL with the JSON definition for 101repo dependencies
wiki101url             | URL       | 
explorer101url         | URL       | 
endpoint101url         | URL       | 
data101url             | URL       | 
