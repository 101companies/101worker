# Runner101::Env

Module to load the runner's environment variables.

## load\_vars

    load_vars(\%vars)

Loads the environment variables given in the hashref `$vars` into the actual
environment `%ENV`. See the `101worker/configs/env/README.md` for
documentation about how these variables should be defined.

Returns nothing useful and might die if ["load\_path"](#load_path) or ["load\_url"](#load_url) dies.

## load\_path

    load_path(\%vars, $value)

Turns a relative into an absolute path and, if necessary, creates its
directories. Returns the resulting absolute path with no trailing slashes.
Dies if the path is invalid.

If `$value` does not end with a slash `/`, it is assumed to be a path to a
file and only the folders preceding it will be created. If it does end with a
slash, it is assumed to be a path to a directory and the full path will be
created as folders. Note that the resulting absolute path will have slashes
stripped though!

    load_path(\%vars, [$ref, $rest])

`$value` may also be a tuple with the first element referencing another key
from `$vars` and the second element being a path relative to that. The `$ref`
is then loaded from `$vars` and the result is joined with the `$rest` before
proceeding. This only makes sense if `$ref` references a directory.

If `$value` contains the text _$worker_ or _$result_, they are replaced with
the absolute paths to the local 101worker and result directory, respectively.

## load\_url

    load_url(\%vars, $value)

Checks if `$value` is a valid URL and returns it again. Dies on an invalid URL.

If the given `$value` is a `file://` URL, its content is first turned into an
absolute path through ["load\_path"](#load_path).
