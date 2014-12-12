# Repo101::Git

Contains a few git functions for pull101repo based on Git::Repository.

## git($repo, @args) or git(@gather\_changes)

Dispatches to `$repo->run(@args)` if a [Git::Repository](https://metacpan.org/pod/Git::Repository) `$repo` is
given as the first argument and to `Git::Repository->run(@args)`
otherwise. Dies if any exit code but `0` is returned by the git command and
propagates the return from the `run` function.

## $null\_tree

Hash for an empty git tree, used to get an initial diff. This hash should
always turn out to be `4b825dc642cb6eb9a060e54bf8d69288fbee4904`. It is used
for getting a sensible `git diff` for a newly cloned repo.

## clone\_or\_pull($dir, $url)

Dispatches to ["clone"](#clone) if the folder `$dir` doesn't exist yet, otherwise
runs ["pull"](#pull). Propagates what the functions return.

## clone($dir, $url)

`git clone`s the repository from `$url` into `$dir`. Returns the changes
between the ["$null\_tree"](#null_tree) and the `HEAD` - see ["gather\_changes"](#gather_changes).

## pull($dir)

`git pull`s the repository in `$dir` and returns the changes between the
revision before the `pull` and the `HEAD` - see ["gather\_changes"](#gather_changes).

## gather\_changes($repo, $from, $to)

Runs a `git diff --name-status` between the two revisions `$from` and `$to`
on the given `$repo`. If one of those revisions is `undef`, the
["$null\_tree"](#null_tree) is used in its place.

Returns a hashref that maps from file path to what happened with the file:
'A' for added, 'M' for modified and 'D' for deleted. Here's an example what
this function could return:

    {
        '/some/path/101repo/added.java' => 'A',
        '/some/path/101repo/modified.c' => 'M',
        '/some/path/101repo/deleted.hs' => 'D',
    }

Usage examples where `$repo` is some [Git::Repository](https://metacpan.org/pod/Git::Repository) instance:

- `gather_changes($repo, undef, 'HEAD')`

    Difference between an empty repository and the current revision. Result will
    be a bunch of additions for every file in the repo.

- `gather_changes($repo, 'HEAD', undef)`

    Same as above, except the return will be a deletion for every file in the repo.

- `gather_changes($repo, 'HEAD^', 'HEAD')`

    The changes from the last commit.
