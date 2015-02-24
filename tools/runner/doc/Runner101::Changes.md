# Runner101::Changes

Gather changes between module runs using the file system's atime (access time)
and mtime (modification time) stamps for each file.

## Note

On many Linux distributions, including Ubuntu, the default setting for atime
is called `relatime`. This is an optimization to prevent writing to the disk
every time a file is accessed, and it will only update the atime if it isn't
already greater than the file's mtime.

This optimization breaks gathering dependencies and you need to turn it off to
use them properly. The setting you want is called `strictatime`.

You can use the command `sudo mount -o remount,strictatime /` (or replace the
`/` with whatever mount point your 101worker is on) to add the strictatime
option during runtime

Alternatively, you can edit your `/etc/fstab` and add the `strictatime`
option to the appropriate mount point to make it permanent.

There is a test in `t/11_changes.t` that will fail if you don't have
`strictatime` enabled, so use that to check for it.

## gather

    gather($time, $module)

Gathers changes that happened after the given `$time` from the 101worker
result directories and writes them to
`$ENV{diffs101dir}/$time.$module.changes`.

Walks through the folders defined by the environment variables
`results101dir`, `temps101dir` and `web101dir` and looks at each file. If a
file has been modified after the given `$time`, a line that looks like
`m $filepath` is written into the output file. If the file has been accessed
after the given `$time`, `a $filepath` is written instead. If neither
occurred, nothing is written.

See the `%.depend` target in `101worker/Makefile` and the script in
`101worker/tools/changes` for how to turn these changes files into graphs.

Also, read the ["Note"](#note), it's important.
