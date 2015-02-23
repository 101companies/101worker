# Runner101::Env

Module to load the runner's environment variables.

## %loaded

    %Runner101::Env::loaded

Cache for already loaded variables.

## load\_vars

    load_vars(\%config)

Loads the environment variables given in `$config` into the actual
environment `%ENV`. See the `101worker/configs/env/README.md` for
documentation about how these variables should be defined.

Returns nothing useful and might die if [load\_var](https://metacpan.org/pod/load_var), ["load\_path"](#load_path) or
["load\_url"](#load_url) dies.

## load\_var

    load_var(\%config, $key)

If ["%loaded"](#loaded) already contains the `$key`, that value is returned.

Otherwise ["load\_path"](#load_path) or ["load\_url"](#load_url) is called, the result is cached in
["%loaded"](#loaded) and then returned.

## load\_path

    load_path(\%config, $value)

Turns a relative into an absolute path and, if necessary, creates its
directories. Returns the resulting absolute path with no trailing slashes.
Dies if the path is invalid.

If `$value` does not end with a slash `/`, it is assumed to be a path to a
file and only the folders preceding it will be created. If it does end with a
slash, it is assumed to be a path to a directory and the full path will be
created as folders. Note that the resulting absolute path will have slashes
stripped though!

All occurrences of `/\$\w+` (that is, variables like `$output` or
`$web101dir`) are replaced with the value they reference, obtained by calling
["load\_var"](#load_var). Circular references will lead to infinite loops.

## load\_url

    load_url(\%config, $value)

Checks if `$value` is a valid URL and returns it again. Dies on an invalid URL.

If the given `$value` is a `file://` URL, its content is first turned into an
absolute path through ["load\_path"](#load_path).
