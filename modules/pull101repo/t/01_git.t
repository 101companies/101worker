#!/usr/bin/perl
use strict;
use warnings;
use Test::More     tests => 22;
use Cwd            qw(abs_path);
use File::Compare;
use File::Slurp    qw(write_file append_file);
use Repo101::Git   qw(clone_or_pull git);

my   $test_dir = abs_path "TEST-01";
my  $local_dir = "$test_dir/local";
my $remote_dir = "$test_dir/remote";
my  $clone_dir = "$test_dir/clone";

sub lives($$) { ok $_[0] || 1, $_[1] }


ok !-e $test_dir, "directory $test_dir doesn't exist yet" or BAIL_OUT;

lives git('init',            $local_dir), 'git init local repo';
lives git('init', '--bare', $remote_dir), 'git init remote repo';
my  $local = Git::Repository->new(work_tree =>  $local_dir);
my $remote = Git::Repository->new(work_tree => $remote_dir);

my @files = qw(test1 test2 test3);
write_file("$local_dir/$_", map { "$_\n" } $_, @files) for @files;
lives git($local, qw(add), @files                      ), 'add test files';
lives git($local, qw(commit -m initial)                ), 'commit test files';
lives git($local, qw(remote add origin), $remote_dir   ), 'remote add origin';
lives git($local, qw(push --set-upstream origin master)), 'push test files';

{
    my $expected = {map { ("$clone_dir/$_" => 'A') } @files};
    is_deeply clone_or_pull($clone_dir, $remote_dir), $expected, 'clone';
    is compare("$clone_dir/$_", "$local_dir/$_"), 0, "$_ identical" for @files;
}

is_deeply clone_or_pull($clone_dir, $remote_dir), {}, 'empty pull';

append_file("$local_dir/test1", "asdf\n");
write_file ("$local_dir/test4", "public static void main(String[] args)\n");
$files[1] = 'test4';
lives git($local, qw(add test1)         ), 'modify test1';
lives git($local, qw(rm  test2)         ), 'remove test2';
lives git($local, qw(add test4)         ), 'add test4';
lives git($local, qw(commit -m modified)), 'commit modifications';
lives git($local, qw(push)              ), 'push modifications';

{
    my $expected = {
        "$clone_dir/test1" => 'M',
        "$clone_dir/test2" => 'D',
        "$clone_dir/test4" => 'A',
    };
    is_deeply clone_or_pull($clone_dir, $remote_dir), $expected, 'pull';
    ok !-e "$clone_dir/test2", 'test2 really removed';
    is compare("$clone_dir/$_", "$local_dir/$_"), 0, "$_ identical" for @files;
}
