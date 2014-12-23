Environment Variable Definitions
================================

Constants for 101worker are defined in environment variables. These consist of file paths and URLs.

All file paths must be given relative to the directory that 101worker is in. They will be turned into absolute paths by the runner. The absolute file paths for directories will never end with a slash.

Constants that contain URLs must end with `url`, like `repo101url`. If a URL variable does not start with a protocol (like `http://` or `https://`), it is assumed to be a file path and will be turned into an absolute `file://` URL.

Examples follow where the path to 101worker is `/var/101worker`.

Definition                                            | Resulting Environment Variable
----------------------------------------------------- | ---------------------------------------------------
repo101       : 101results/101repo                    |       repo101=/var/101results/101repo
gitdeps101    : 101results/gitdeps/                   |    gitdeps101=/var/101results/gitdeps
repo101url    : test/reposource                       |    repo101url=file:///var/test/reposource
gitdeps101url : http://101companies.org/pullRepo.json | gitdeps101url=http://101companies.org/pullRepo.json

const101.py
-----------

This is intended to replace `libraries/101meta/const101.py`, which is just a Python module that holds a bunch of hard-coded strings, which is redundant with the existence of environment variables and inflexible because it can't be fed different values for testing.

The const101 Python module is therefore deprecated and all instances using it should be using `os.environ` instead (see below).

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
