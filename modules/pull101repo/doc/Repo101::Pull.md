# Repo101::Pull

Class for managing 101repo with its dependencies and gathering changes between
revisions.

## Attributes

An object of this class has the following attributes, some of which are
required to be given in the constructor (`Repo101::Pull->new(%args)`) and
when calling ["pull101repo"](#pull101repo):

- root\_path

    File system path to where 101repo should be pulled to. Required and must be an
    absolute path.

- root\_url

    Remote path of 101repo. Doesn't actually need to be a URL, it can be any remote
    path that git can handle. Required.

- deps\_path

    File system path to where gitdeps should be pulled to. Required and must be an
    absolute path.

- repos

    Repo list as per http://101companies.org/pullRepo.json. Required.

    The repo list is a mapping of namespaces (like contributions, modules, services
    etc.) to namespace members. Each namespace member is a mapping from the member
    name (like simpleJava or refineTokens) to the GitHub URL, which may include
    a sub-directory in the master branch. See the tests in `t/02_extract_repo_info`
    to see which paths are allowed.

- changes

    A hash mapping from a file path relative to the `root_path` to a change
    operation: 'A' for added, 'M' for modified and 'D' for deleted. Defaults to an
    empty hash and gets filled when repos are pulled.

- pulled

    A hash mapping from a repo URL to raw changes obtained via `git diff`. Used
    internally to see which repos are already pulled and to merge into `changes`.

- branches

    A mapping from URL to branch name. If an entry like this exists for a given
    repo URL, the given branch is checked out. This is used in
    [101test](https://github.com/101companies/101test) to simulate changes in
    101repo without having to actually change anything.

- changes

    Buffer for gathered diffs over all pulled repos. Defaults to an empty hashref,
    which is probably the Right Thing to start out with.

- pulled

    Which repos have already been pulled during this run, avoids calling git
    repeatedly for contributions from the same repo. Defaults to an empty hashref,
    which is also the Right Thing to start with.

## pull101repo

    my $changes = pull101repo(
        root_path => $root_path,
        deps_path => $deps_path,
        root_url  => $root_url,
        repos     => \%repos,
        # optional, used for 101test
        branches  => \%branches,
    );

This is probably what you want to call. It pulls the root repo, pulls all
dependent repos and symlinks them into the root repo and cleans up removed
symlinks and dependent repos. Returns a hashref of changes with paths relative
to the given `root_path`.

The arguments map to the attributes described in ["Attributes"](#attributes) above.

## pull\_namespace

    $self->pull_namespace($namespace)

Pulls all members of the given namespace - see ["pull\_member"](#pull_member). Warns if
something goes wrong in any of those pulls. Also ["clean\_link"](#clean_link)s the symlinks
that aren't members anymore.

Returns nothing of use.

## pull\_member

    $self->pull_member($repo, $diff_path, $link_path)

["pull\_repo"](#pull_repo)s the given repo, then ["merge\_diff"](#merge_diff)s the resulting diff using
the given `$diff_path` as the new path and finally ["symlink"](#symlink)s the member
into the 101repo folder.

Returns nothing useful, but virtually every step of the above can die. Catch
these exceptions like ["pull\_namespace"](#pull_namespace) does.

## pull\_repo

    $self->pull_repo($path, $url)

Clones or pulls the repo from the given `$url` into the given `$dir`ectory.
The raw diff is stored in `$self->pulled->{$url}`, if that value
already exists the repo isn't pulled again. Returns that raw diff.

## merge\_diffs

    $self->merge_diffs($diff, $oldpath=$self->root_path, $newpath=undef)

Merges the changes from the given `$oldpath` in `$diff` into
`$self->changes` under the given `$newpath` if it's defined.

If an entry in the `$diff` starts with the given `$oldpath`, it is deleted
from `$diff` and inserted into `$self->changes`. Its path will have
`"$oldpath/"` stripped and, if it is defined, have `"$newpath/"` prefixed.

Returns `$self->changes`.

## extract\_repo\_info

     $self->extract_repo_info($url)

Extracts user name, repo name and suffix path (if given) from a GitHub repo URL.
Returns `undef` if the user is `101companies` and the repo is `101repo`,
because we don't care about pulling the root repo a bunch of times. Otherwise
returns a hashref with the following contents:

- repo\_path

    The local path where the repo should be cloned or pulled to.

- repo\_url

    The remote URL of the repo. This URL will start with
    `https://git::@github.com`, the `git::@` thing meaning that no username and
    password should be used, which is necessary because a password prompt locks up
    everything.

- dep\_path

    The path inside of the contribution that should be symlinked to. Will be
    identical to the `repo_path` if no suffix path is given in the URL.

See also the tests in `t/02_extract_repo_info`.

## symlink

    $self->symlink($src, $dst)

Creates a symlink at `$dst` pointing to the directory `$src`. If `$dst`
already exists, it is removed first. Returns nothing useful.

## clean\_link

    $self->clean_link($repos, $link)

If the given `$link` really is a symlink and it is not a member in the
`$repos` hashref, the `$link` and whatever it points to is deleted and the
deletions are added to `$self->diff`.

If `$link` isn't a symlink or it's still a member of `$repos`, this does
nothing.

Returns nothing useful.
