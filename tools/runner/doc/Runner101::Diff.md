# Runner101::Diff

Contains functions to handle the diff protocol between the runner and modules.

## Diff Protocol

The diff protocol is a simple line-based protocol.

See `101worker/libraries/incremental101` for a Python library for this
protocol, use that instead of writing a new implementation.

### Output From Module

The modules output the diff lines to their stdout. Any line that the runner
can't parse will be ignored and printed instead, because a lot of worker
modules are very wordy.

Each line has the following elements, separated by whitespace:

- lines read so far

    The number of lines of diff that the module has read. Should be used for error
    recovery sometime.

- operation

    What has been done to the file. This may be `A` for an added file, `M` for a
    modified file and `D` for a deleted file.

- file path

    The path to the file. Shall be an absolute path.

Operation and file path may _both_ be a single hyphen `-`, in case the module
just wants to tell the runner how many input lines it has read so far.

### Input To Module

The modules receive the diff lines to their stdin. Any line that a module can't
parse should cause the module to fail, because the runner isn't supposed to
output garbage.

Each line has the following elements, separated by whitespace, which work the
same way as above:

- operation
- file path

## parse

    parse($line, \@diffs)

Attempts to parse `$line` as a diff. If there's anything interesting in it,
it will be pushed to the `$diffs` arrayref. Returns the _lines read so far_
if it could parse the line and `undef` otherwise.

## run\_diff

    run_diff(\@command, \@diffs, $log, $wantdiff)

Executes the given `$command`, which is an arrayref containing the arguments
of the command. If `$wantdiff` is true, the given `$diffs` are piped into
it. The stdandard error of the command goes into the givnen `$log` filehandle.

After the command ran, its output is ["parse"](#parse)d for diff output (even if
`$wantdiff` is false!) and any diffs found are added to the given `$diffs`.
Any other output is appended to the given `$log` filehandle. Note that this
means that the log will contain all stderr first and then all stdout.

Returns the exit code of the process run and warns on errors like broken pipe.
