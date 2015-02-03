Environment Variable Definitions
================================

Constants for 101worker are defined in environment variables. These consist of file paths, directory paths and URLs.

File paths and directory paths are similar to each other: they are given relative to the directory that the 101worker directory is in and will be turned into absolute paths by the runner. Directory paths *must* and file paths *must not* not end with a slash, that way the runner can disambiguate between a file and a directory paths. All directories that appear in any path will be created automatically if they don't exist. Nonexistent files will *not* be created (which is why there is a need for disambiguation). However, the resulting environment variables *will never have a trailing slash*!

You can reference the absolute paths to the worker and the absolute path to the result directory using *$worker* and *$results* respectively.

You can also reference other paths by their key. For example, if there is the definition like `dumps101dir : 101web/data/dumps/`, then you can reference that path like `wiki101dump : [dumps101dir, wiki.json]`. The result will be `wiki101dump=/path/to/worker/101web/data/dumps/wiki.json`.

URLs are only special if they start with the `file://` scheme. In that case, their path will be turned into an absolute `file://` URL as described above. The same rule for trailing slashes apply. Other URLs like `http://` or `https://` won't be touched.

For examples, see the definition files in the folder of this README.

Intent
------

This is primarily intended to replace `libraries/101meta/const101.py`, which is just a Python module that holds a bunch of hard-coded strings, which is silly and inflexible. It also replaces the redundant definitions in `101worker/Makefile.vars` and probably various other Makefiles and hard-coded paths in modules.

The environment variable approach fulfills the “Single Point of Truth” or “Once and Only Once” rule: they are defined in one place and can be accessed from virtually any programming environment. It is also much more flexible and allows creation of a test environment.

The const101 Python module and Makefile.vars are therefore *deprecated* and will hopefully be removed soon.

Accessing Environment Variables
-------------------------------

Getting a value from an environment variable is utterly trivial in virtually any language. Here's examples on how to do it in the various languages used in 101worker.

```python
#!/usr/bin/env python
# os.environ is a dict with the environment
import os
repo_path = os.environ['repo101'   ]
repo_url  = os.environ['repo101url']
```

```perl
#!/usr/bin/perl
# %ENV is a hash with the environment
my $repo_path = $ENV{repo101   };
my $repo_url  = $ENV{repo101url};
```

```ruby
#!/usr/bin/env ruby
# ENV is a hash with the environment
repo_path = ENV['repo101'   ]
repo_url  = ENV['repo101url']
```

```php
<?php
// $_ENV is a superglobal array with the environment
$repo_path = $_ENV['repo101'   ];
$repo_url  = $_ENV['repo101url'];
```

Constant Documentation
----------------------

These are the constants that are currently in use.

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
