#!/usr/bin/perl
use strict;
use warnings;
use Test::More    tests => 6;
use Cwd           qw(abs_path);
use File::Slurp   qw(write_file append_file);
use Repo101::Git  qw(clone_or_pull git);
use Repo101::Pull qw(pull101repo);


sub init_repo
{
    my $dir = shift;
    git('init', @_, $dir);
    Git::Repository->new(work_tree => $dir)
}

sub add_repo_files
{
    my ($repo, $dir, $files) = @_;
    while (my ($file, $data) = each %$files)
    {
        my $path = "$dir/$file";
        if (ref $data)
        {
            mkdir $path or die "Couldn't mkdir $path: $!";
            add_repo_files($repo, $path, $data);
        }
        else
        {
            write_file($path, $data);
            git($repo, 'add', $path);
        }
    }
}

sub build_repo
{
    my %arg      = @_;
    my $local    = init_repo($arg{local});
    my $remote   = init_repo($arg{remote}, '--bare');

    add_repo_files($local, $arg{local}, $arg{files});

    git($local, qw(commit -qm initial)                  );
    git($local, qw(remote add origin), $arg{remote}     );
    git($local, qw(push -q --set-upstream origin master));

    ($local, $remote)
}


my $test_dir = abs_path('TEST') . "/changes$$";

my ($local_repo, $remote_repo) = build_repo(
    local  => "$test_dir/local/101repo",
    remote => "$test_dir/remote/101repo",
    files  => {
        'README.md'   => "Test readme.\n",
        'Class.java'  => "public static final class\n",
        contributions => {
            repo_contribution => {
                'README.md' => "Contribution directly in 101repo\n",
            },
        },
    },
);

my ($local_dep1, $remote_dep1) = build_repo(
    local  => "$test_dir/local/dep1",
    remote => "$test_dir/remote/dep1",
    files  => {
        'README.md'  => "dep1 readme.\n",
        'Class.java' => "public static final class\n",
    },
);


my $repos = {
    contributions => {
        dependency1 => "$test_dir/gitdeps/dep1\t$test_dir/remote/dep1",
    },
};

# monkey-patch
{
    no warnings 'redefine';
    *Repo101::Pull::extract_repo_info = sub
    {
        my ($self, $url)              = @_;
        my ($local, $remote, $suffix) = split /\t/, $url;
        {
            repo_path => $local,
            repo_url  => $remote,
            dep_path  => $suffix ? "$local/$suffix" : $local,
        }
    };
}


my %pull = (
    root_path => "$test_dir/101repo",
    deps_path => "$test_dir/gitdeps",
    root_url  => $remote_repo->work_tree,
    repos     => $repos,
);

is_deeply pull101repo(%pull), {
              'README.md'                                  => 'A',
              'Class.java'                                 => 'A',
              'contributions/repo_contribution/README.md'  => 'A',
              'contributions/dependency1/README.md'        => 'A',
              'contributions/dependency1/Class.java'       => 'A',
          }, 'clone';

is_deeply pull101repo(%pull), {}, 'empty pull';

for ($local_repo, $local_dep1)
{
    write_file ($_->work_tree . "/added", "added file\n");
    append_file($_->work_tree . "/Class.java", "private class Class\n");
    git($_, 'add', 'added', 'Class.java');
    git($_, 'rm', 'README.md');
    git($_, 'commit', '-qm', 'modified');
    git($_, 'push', '-q');
}

is_deeply pull101repo(%pull), {
              'added'                                => 'A',
              'Class.java'                           => 'M',
              'README.md'                            => 'D',
              'contributions/dependency1/added'      => 'A',
              'contributions/dependency1/Class.java' => 'M',
              'contributions/dependency1/README.md'  => 'D',
          }, 'pull';


delete $repos->{contributions}{dependency1};
is_deeply pull101repo(%pull), {
              'contributions/dependency1/added'      => 'D',
              'contributions/dependency1/Class.java' => 'D',
          }, 'delete pull';
ok !-e "$test_dir/101repo/dependency1", 'symlink deleted';
ok !-e "$test_dir/gitdeps/dep1",        'real folder deleted';
