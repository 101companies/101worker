package Repo101::Pull;
use Exporter qw(import);
@EXPORT_OK = qw(pull101repo);

use strict;
use warnings;
use File::Basename qw(basename);
use File::Path     qw(remove_tree);
use Repo101::Git   qw(clone_or_pull);

use Class::Tiny {
    root_path => undef,
    root_url  => undef,
    deps_path => undef,
    repos     => undef,
    changes   => sub { {} },
    pulled    => sub { {} },
};


sub pull101repo
{
    my $self = __PACKAGE__->new(@_);

    $self->merge_diffs($self->pull_repo($self->root_path, $self->root_url));

    for my $namespace (keys %{$self->repos})
    {
        my $namespace_dir = join '/', $self->root_path, $namespace;

        if (!-e $namespace_dir)
        {   mkdir $namespace_dir or die "Couldn't create $namespace_dir: $!" }

        my $repos = $self->repos->{$namespace};
        for my $member (keys %$repos)
        {
            my $info = $self->extract_repo_info($repos->{$member}) or next;
            my $diff = $self->pull_repo($info->{repo_path}, $info->{repo_url});
            $self->merge_diffs($diff, $info->{dep_path}, "$namespace/$member");
            $self->symlink($info->{dep_path}, "$namespace_dir/$member");
        }

        $self->clean_link($repos, $_) for glob "$namespace_dir/*";
    }

    $self->changes
}


sub pull_repo
{
    my ($self, $dir, $url) = @_;
    $self->pulled->{$url} = clone_or_pull($dir, $url)
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
        repo_url  => "https://github.com/$user/$repo_name",
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


1 # The Magic One, don't remove it because that might make require fail.
__END__

=head1 Repo101::Pull

Class for managing 101repo with its dependencies and gathering changes between
revisions.

=head2 Class

An object of this class has the following attributes, some of which are
required to be given in the constructor and when calling L</pull101repo>:

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

Repo list as per http://101companies.org/pullRepo.json TODO. Required.

=item changes

A hash mapping from a file path relative to the C<root_path> to a change
operation: 'A' for added, 'M' for modified and 'D' for deleted. Defaults to an
empty hash and gets filled when repos are pulled.

=item pulled

A hash mapping from a repo URL to raw changes obtained via C<git diff>. Used
internally to see which repos are already pulled and to merge into C<changes>.

=back

=head2 pull101repo(:root_path, :root_url, :deps_path, :repos)

This is probably what you want to call. It pulls the root repo, pulls all
dependent repos and symlinks them into the root repo and cleans up removed
symlinks and dependent repos. Returns a hashref of changes with paths relative
to the given C<root_path>.

This sub takes a hash of named arguments and forwards them to the constructor,
so you call it like this:

    my $changes = pull101repo(
        root_path => $root_path,
        deps_path => $deps_path,
        root_url  => $root_url,
        repos     => $repos,
    );

The arguments map to the attributes described in the L</Class> section above.

=head2 $self->pull_repo($path, $url)

Clones or pulls the repo from the given C<$url> into the given C<$dir>ectory.
The raw diff is stored in C<< $self->pulled->{$url} >>, if that value
already exists the repo isn't pulled again. Returns that raw diff.

=head2 $self->merge_diffs($diff, $oldpath = $self->root_path, $newpath = undef)

Merges the changes from the given C<$oldpath> in C<$diff> into
C<< $self->changes >> under the given C<$newpath> if it's defined.

If an entry in the C<$diff> starts with the given C<$oldpath>, it is deleted
from C<$diff> and inserted into C<< $self->changes >>. Its path will have
C<"$oldpath/"> stripped and, if it is defined, have C<"$newpath/"> prefixed.

Returns C<< $self->changes >>.

=head2 $self->extract_repo_info($url)

TODO

=head2 $self->symlink($src, $dst)

Creates a symlink at C<$dst> pointing to C<$src>. If C<$dst> already exists, it
is removed first.

=head2 $self->clean_link($repos, $link)

TODO

=cut
