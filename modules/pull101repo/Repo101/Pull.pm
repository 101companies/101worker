package Repo101::Pull;
use Class::Tiny qw(root_path root_url deps_path repos), {
    changes => sub { {} },
    pulled  => sub { {} },
};
use Exporter qw(import);
@EXPORT = qw(pull101repo extract_repo_info);

use strict;
use warnings;
use File::Basename qw(basename);
use File::Path     qw(remove_tree);
use Repo101::Git   qw(clone_or_pull);


sub pull101repo
{
    my $self = __PACKAGE__->new(@_);

    $self->pull_repo($self->root_path, $self->root_url);

    for my $namespace (keys %{$self->repos})
    {
        my $namespace_dir = join '/', $self->root_path, $namespace;

        if (!-e $namespace_dir)
        {   mkdir $namespace_dir or die "Couldn't create $namespace_dir: $!" }

        my $repos = $self->repos->{$namespace};
        for my $member (keys %$repos)
        {
            my $info = $self->extract_repo_info($repos->{$member}) or next;
            $self->pull_repo($info->{repo_path}, $info->{repo_url},
                             "$namespace/$member");
            $self->symlink($info->{dep_path}, "$namespace_dir/$member");
        }

        $self->clean_link($repos, $_) for glob "$namespace_dir/*";
    }

    $self->changes
}


sub pull_repo
{
    my ($self, $path, $url, $newpath) = @_;
    $self->pulled->{$url} = clone_or_pull($path, $url)
        if not exists $self->pulled->{$url};
    $self->merge_changes($self->pulled->{$url}, $path, $newpath)
}


sub merge_changes
{
    my ($self, $new, $oldpath, $newpath) = @_;
    $oldpath //= $self->root_path;

    my $regex = quotemeta $oldpath;
    for (keys %$new)
    {
        if (m{^$regex/(.+)$})
        {
            my $key = defined $newpath ? "$newpath/$1" : $1;
            $self->changes->{$key} = $new->{$_};
            delete $new->{$_};
        }
    }
}


sub extract_repo_info
{
    my ($self, $url) = @_;

    $url =~ m{https://github\.com/([^/]+)/([^/]+)(?:/tree/master/?(.*))?$}
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
    unlink $dst if -e $dst && -l $dst;
    symlink($src, $dst) || die "Couldn't link $src to $dst: $!" if not -e $dst;
}


sub clean_link
{
    my ($self, $repos, $link) = @_;
    return if not -l $link;

    my $member = basename($link);
    return if exists $repos->{$member};

    my $real    = readlink $link or die "Couldn't resolve $link: $!";
    my $repo    = Git::Repository->new(work_tree => $link);
    my $deleted = Repo101::Git::gather_changes($repo, 'HEAD', undef);
    my $newpath = substr $link, 1 + length $self->root_path;
    $self->merge_changes($deleted, $real, $newpath);

    unlink      $link  or die "Couldn't remove link $link: $!";
    remove_tree($real) or die "Couldn't remove file $real: $!";
}
