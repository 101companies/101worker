package Repo101::Pull;
use Exporter qw(import);
@EXPORT_OK = qw(pull101repo);

use strict;
use warnings;
use File::Basename qw(basename);
use File::Path     qw(remove_tree);
use Repo101::Git   qw(clone_or_pull);
use Try::Tiny;

use Class::Tiny {
    root_path => undef,
    root_url  => undef,
    deps_path => undef,
    repos     => undef,
    branches  => sub { {} },
    changes   => sub { {} },
    pulled    => sub { {} },
};


sub pull101repo
{
    my $self = __PACKAGE__->new(@_);
    $self->merge_diffs($self->pull_repo($self->root_path, $self->root_url));
    $self->pull_namespace($_) for keys %{$self->repos};
    $self->changes
}


sub pull_namespace
{
    my ($self, $namespace) = @_;
    my  $namespace_dir     = join '/', $self->root_path, $namespace;

    if (!-d $namespace_dir)
    {   mkdir $namespace_dir or die "Couldn't create $namespace_dir: $!" }

    my $repos = $self->repos->{$namespace};
    for my $member (keys %$repos)
    {
        my $diff_path = "$namespace/$member";
        my $link_path = "$namespace_dir/$member";
        try
        {   $self->pull_member($repos->{$member}, $diff_path, $link_path) }
        catch
        {   warn "Error in member $member: $_" };
    }

    $self->clean_link($repos, $_) for glob "$namespace_dir/*";
}


sub pull_member
{
    my ($self, $repo, $diff_path, $link_path) = @_;

    my $info = $self->extract_repo_info($repo) or return;
    my $diff = $self->pull_repo($info->{repo_path}, $info->{repo_url});

    $self->merge_diffs($diff, $info->{dep_path}, $diff_path);
    $self->symlink($info->{dep_path}, $link_path);
}


sub pull_repo
{
    my ($self, $dir, $url) = @_;
    $self->pulled->{$url} = clone_or_pull($dir, $url, $self->branches->{$url})
        if not exists $self->pulled->{$url};
    $self->pulled->{$url}
}


sub merge_diffs
{
    my ($self, $diff, $oldpath, $newpath) = @_;
    my $changes                           = $self->changes;

    my $regex = quotemeta($oldpath // $self->root_path);
    for (keys %$diff)
    {
        if (m{^$regex/(.+)$})
        {
            my $key = defined $newpath ? "$newpath/$1" : $1;
            die "Already got a diff entry for $key" if exists $changes->{$key};
            $changes->{$key} = delete $diff->{$_};
        }
    }

    $changes
}


sub extract_repo_info
{
    my ($self, $url) = @_;

    $url =~ m{^https://github\.com/([^/]+)/([^/]+)(?:/tree/master/?(.*))?$}
        or die "Couldn't match repository URL: $url";
    my ($user, $repo_name, $suffix) = ($1, $2, $3);

    return undef if $user eq '101companies' && $repo_name eq '101repo';

    my %info = (
        repo_path => $self->deps_path . "/$user/$repo_name",
        repo_url  => "https://git::\@github.com/$user/$repo_name",
    );
    $info{dep_path} = $suffix ? "$info{repo_path}/$suffix" : $info{repo_path};

    \%info
}


sub symlink
{
    my (undef, $src, $dst) = @_;
    die "Not a directory: $src" if not -d $src;
    unlink $dst                 if     -e $dst;
    symlink $src, $dst or die "Couldn't link $src to $dst: $!";
}


sub clean_link
{
    my ($self, $repos, $link) = @_;
    return if not -l $link;

    my $member = basename($link);
    return if exists $repos->{$member};

    my $real    = readlink $link;
    die "Couldn't resolve $link: $!" unless $real && -d $real;
    my $repo    = Git::Repository->new(work_tree => $link);
    my $deleted = Repo101::Git::gather_changes($repo, 'HEAD', undef);
    my $newpath = substr $link, 1 + length $self->root_path;
    $self->merge_diffs($deleted, $real, $newpath);

    unlink      $link  or die "Couldn't remove link $link: $!";
    remove_tree($real) or die "Couldn't remove file $real: $!";
}


1
__END__

=head1 Repo101::Pull

Class for managing 101repo with its dependencies and gathering changes between
revisions.

=head2 Attributes

An object of this class has the following attributes, some of which are
required to be given in the constructor (C<< Repo101::Pull->new(%args) >>) and
when calling L</pull101repo>:

=over

=item root_path

File system path to where 101repo should be pulled to. Required and must be an
absolute path.

=item root_url

Remote path of 101repo. Doesn't actually need to be a URL, it can be any remote
path that git can handle. Required.

=item deps_path

File system path to where gitdeps should be pulled to. Required and must be an
absolute path.

=item repos

Repo list as per http://101companies.org/pullRepo.json. Required.

The repo list is a mapping of namespaces (like contributions, modules, services
etc.) to namespace members. Each namespace member is a mapping from the member
name (like simpleJava or refineTokens) to the GitHub URL, which may include
a sub-directory in the master branch. See the tests in C<t/02_extract_repo_info>
to see which paths are allowed.

=item changes

A hash mapping from a file path relative to the C<root_path> to a change
operation: 'A' for added, 'M' for modified and 'D' for deleted. Defaults to an
empty hash and gets filled when repos are pulled.

=item pulled

A hash mapping from a repo URL to raw changes obtained via C<git diff>. Used
internally to see which repos are already pulled and to merge into C<changes>.

=item branches

A mapping from URL to branch name. If an entry like this exists for a given
repo URL, the given branch is checked out. This is used in
L<101test|https://github.com/101companies/101test> to simulate changes in
101repo without having to actually change anything.

=item changes

Buffer for gathered diffs over all pulled repos. Defaults to an empty hashref,
which is probably the Right Thing to start out with.

=item pulled

Which repos have already been pulled during this run, avoids calling git
repeatedly for contributions from the same repo. Defaults to an empty hashref,
which is also the Right Thing to start with.

=back

=head2 pull101repo

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
to the given C<root_path>.

The arguments map to the attributes described in L</Attributes> above.

=head2 pull_namespace

    $self->pull_namespace($namespace)

Pulls all members of the given namespace - see L</pull_member>. Warns if
something goes wrong in any of those pulls. Also L</clean_link>s the symlinks
that aren't members anymore.

Returns nothing of use.

=head2 pull_member

    $self->pull_member($repo, $diff_path, $link_path)

L</pull_repo>s the given repo, then L</merge_diff>s the resulting diff using
the given C<$diff_path> as the new path and finally L</symlink>s the member
into the 101repo folder.

Returns nothing useful, but virtually every step of the above can die. Catch
these exceptions like L</pull_namespace> does.

=head2 pull_repo

    $self->pull_repo($path, $url)

Clones or pulls the repo from the given C<$url> into the given C<$dir>ectory.
The raw diff is stored in C<< $self->pulled->{$url} >>, if that value
already exists the repo isn't pulled again. Returns that raw diff.

=head2 merge_diffs

    $self->merge_diffs($diff, $oldpath=$self->root_path, $newpath=undef)

Merges the changes from the given C<$oldpath> in C<$diff> into
C<< $self->changes >> under the given C<$newpath> if it's defined.

If an entry in the C<$diff> starts with the given C<$oldpath>, it is deleted
from C<$diff> and inserted into C<< $self->changes >>. Its path will have
C<"$oldpath/"> stripped and, if it is defined, have C<"$newpath/"> prefixed.

Returns C<< $self->changes >>.

=head2 extract_repo_info

     $self->extract_repo_info($url)

Extracts user name, repo name and suffix path (if given) from a GitHub repo URL.
Returns C<undef> if the user is C<101companies> and the repo is C<101repo>,
because we don't care about pulling the root repo a bunch of times. Otherwise
returns a hashref with the following contents:

=over

=item repo_path

The local path where the repo should be cloned or pulled to.

=item repo_url

The remote URL of the repo. This URL will start with
C<https://git::@github.com>, the C<git::@> thing meaning that no username and
password should be used, which is necessary because a password prompt locks up
everything.

=item dep_path

The path inside of the contribution that should be symlinked to. Will be
identical to the C<repo_path> if no suffix path is given in the URL.

=back

See also the tests in C<t/02_extract_repo_info>.

=head2 symlink

    $self->symlink($src, $dst)

Creates a symlink at C<$dst> pointing to the directory C<$src>. If C<$dst>
already exists, it is removed first. Returns nothing useful.

=head2 clean_link

    $self->clean_link($repos, $link)

If the given C<$link> really is a symlink and it is not a member in the
C<$repos> hashref, the C<$link> and whatever it points to is deleted and the
deletions are added to C<< $self->diff >>.

If C<$link> isn't a symlink or it's still a member of C<$repos>, this does
nothing.

Returns nothing useful.

=cut
