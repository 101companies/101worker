# Repo101::Git

Contains a few git functions for pull101repo based on Git::Repository.

## git

    git(@args)
    git(Git::Repository $repo, @args)

Dispatches to `$repo->run(@args)` if a [Git::Repository](https://metacpan.org/pod/Git::Repository) `$repo` is
given as the first argument and to `Git::Repository->run(@args)`
otherwise. Dies if any exit code but `0` is returned by the git command and
propagates the return from the `run` function.

## null\_tree

    $null_tree

Hash for an empty git tree, used to get an initial diff. This hash should
always turn out to be `4b825dc642cb6eb9a060e54bf8d69288fbee4904`. It is used
for getting a sensible `git diff` for a newly cloned repo.

## clone\_or\_pull

    clone_or_pull($dir, $url)
    clone_or_pull($dir, $url, $branch)

Dispatches to ["clone"](#clone) if the folder `$dir` doesn't exist yet, otherwise
runs ["pull"](#pull). If a `$branch` is given, it will also run `git checkout` on
it. This is used in [101test](https://github.com/101companies/101test).

Returns a diff of changes between the previous and the current state - see
["gather\_changes"](#gather_changes).

## clone

    clone($dir, $url)

`git clone`s the repository from `$url` into `$dir`. Returns a two-element
list containing the resulting `Git::Repository` and `undef` (because there
was no previous revision).

See also ["pull"](#pull) and ["clone\_or\_pull"](#clone_or_pull).

## pull

    pull($dir)

`git pull`s the repository in `$dir`. Returns a two-element list containing
the `Git::Repository` and the revision before the pull.

See also ["clone"](#clone) and ["clone\_or\_pull"](#clone_or_pull).

## gather\_changes

    gather_changes($repo, $from=$null_tree, $to=$null_tree)

Runs a `git diff --name-status` between the two revisions `$from` and `$to`
on the given `$repo`. If any one of those revisions is not given or `undef`,
the ["$null\_tree"](#null_tree) is used in its place.

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
