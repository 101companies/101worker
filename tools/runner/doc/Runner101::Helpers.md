# Runner101::Helpers

Contains a few helper functions used in various places of the runner.

## slurp\_json

    slurp_json($path)

Reads the contents of the file given in `$path` and JSON-decodes its content.
Returns the decoding result or dies if an error reading or decoding occurs.

## spew\_json

    spew_json($path, $content)

JSON-encodes the given `$content` and writes it to the file at `$path`.
Returns nothing useful and dies if an error encoding or writing the file occurs.

## guess\_json

    guess_json($thing = $_)

`$thing` may either be a reference, a JSON string or a file path. This
function figures out which kind of `$thing` it was given and JSON-decodes it
into a data structure. Returns the result and dies on error.

Defaults to `$_` if `$thing` is not given.

More specifically, if `$thing` is a reference, it is assumed to be already
decoded and it is returned unchanged. Otherwise, if it's a string with the
first non-whitespace character being `{` or `[`, it is assumed to be a JSON
object or array respectively (JSON only supports those two as top-level
structures) and is JSON-decoded. If that's also not the case, it is assumed to
be a file path and it is ["slurp\_json"](#slurp_json)'d.

## validate\_json

    validate_json($json, $schema)

Validates `$json` against the given JSON-`$schema`. Both parameters are
["guess\_json"](#guess_json)'d, so they may each be a hash, an array, a JSON string or a path
to a JSON file.

Returns the (decoded, if necessary) `$json` on successful validation and dies
with a diagnostic message on validation failure.

## write\_log

    write_log(@message)

Prints the current date and time, its arguments and then a newline.
