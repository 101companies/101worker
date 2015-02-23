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

## merge\_diff

    merge_diff($diff, $op, $file)

Merges the given `$file` and `$op`eration into the given `$diff`. If the
`$file` isn't yet in `$diff`, it will just be inserted. Otherwise, the
result will be chosen so that the end result reflects the actual state of
the file system, according to the following table:

    $diff $op $resolved
      A    M      A
      A    D
      M    M      M
      M    D      D
      D    A      M
      A    A      A
      M    A      M
      D    M      M
      D    D      D

Returns the operation that the merge resolved to. Dies if a set of operations
can't be resolved, which should only happen if there's an invalid operation
present that isn't `A`, `M` or `D`.

## merge\_diffs

    merge_diffs($old, $new)

Merges two entire diffs and returns the merged diff. None of the input values
are modified.

See ["merge\_diff"](#merge_diff) about how individual operations are resolved.

## parse

    parse($line, \@diffs)

Attempts to parse `$line` as a diff. If there's anything interesting in it,
it will be pushed to the `$diffs` arrayref. Returns the _lines read so far_
if it could parse the line and `undef` otherwise.

## store\_diff

    store_diff($name, $diff)

Stores the given `$diff` in a file called `$ENV{diffs101dir}/$name.diff`.
Any existing file of that name will be clobbered.

Returns nothing useful and dies if the file can't be written to.

See also ["load\_stored"](#load_stored) and ["remove\_stored"](#remove_stored).

## load\_stored

    load_stored($name)

Attempts to load a diff that was previously stored with the same `$name` via
["store\_diff"](#store_diff).

Returns the loaded diff or an empty diff if there was no file to load anything
from. Dies if the file exists, but can't be read.

See also ["store\_diff"](#store_diff) and ["remove\_stored"](#remove_stored).

## remove\_stored

    remove_stored($name)

Attempts to removes a diff file that was previously stored with the same
`$name` via ["store\_diff"](#store_diff).

Returns true if there was a file and it was deleted, or false if there was no
file to be deleted. Dies if the file exists, but can't be deleted.

See also ["store\_diff"](#store_diff) and ["load\_stored"](#load_stored).

## build\_diff

    build_diff($module, $current, $log)

Builds a diff for the given `$module`.

If it doesn't want a diff, an empty diff is returned.

If it does want a diff and there is a previously stored diff (see
["store\_diff"](#store_diff)), it is recovered (see ["load\_stored"](#load_stored) and merged with the
result diff from the previous run and the given `$current` diff (see
["merge\_diffs"](#merge_diffs)). The fact that this happened is logged to `$log`. The
resulting diff is returned.

Otherwise, if there is no stored diff to be recovered, it returns the given
`$current` diff.

## run\_diff

    run_diff(Runner101::Module $module, $diff, $log)

Builds a diff for the given `$module`, as per ["build\_diff"](#build_diff). Then runs the
`$module`'s command.

After the command ran, its output is ["parse"](#parse)d for diff output (even if
`$module->wantdiff` is false!) and any diffs found are added to the given
`$diff`.

Any other output is appended to the given `$log` filehandle. Note that this
means that the log will contain all stderr first and then all stdout.

If the `$module` takes a diff as input and the command exited with a non-zero
status, the diff is stored via ["store\_diff"](#store_diff). Otherwise, any stored diff that
might have existed is removed via `/remove_diff`.

Returns the exit code of the process run and warns on errors like broken pipe.
