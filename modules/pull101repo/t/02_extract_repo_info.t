#!/usr/bin/perl
use strict;
use warnings;
use Test::More tests => 9;
use Test::Exception;
use Repo101::Pull qw(extract_repo_info);

my $g = 'https://github.com';

my $pull = Repo101::Pull->new(
    root_path => "/test/101repo",
    deps_path => "/test/gitdeps",
    root_url  => "$g/101companies/101repo",
    repos     => {},
);

my $expected = {
    repo_path => '/test/gitdeps/user/repo',
    dep_path  => '/test/gitdeps/user/repo',
    repo_url  => "$g/user/repo",
};

is_deeply $pull->extract_repo_info("$g/user/repo"),
          $expected, 'just a repo URL';

is_deeply $pull->extract_repo_info("$g/user/repo/tree/master"),
          $expected, 'repo URL with tree/master';

is_deeply $pull->extract_repo_info("$g/user/repo/tree/master/"),
          $expected, 'repo URL with tree/master/';

$expected->{dep_path} .= '/suffix/path';
is_deeply $pull->extract_repo_info("$g/user/repo/tree/master/suffix/path"),
          $expected, 'repo URL with tree/master/ and a suffix';

is_deeply $pull->extract_repo_info("$g/101companies/101repo"),
          undef, '101companies/101repo gets skipped';

dies_ok { $pull->extract_repo_info("$g/user/repo/") }
        'excessive slash fails';

dies_ok { $pull->extract_repo_info("$g/user") }
        'missing repo fails';

dies_ok { $pull->extract_repo_info("$g/user/repo/tree/dev") }
        'non-master tree fails';

dies_ok { $pull->extract_repo_info("https://github,com/user/repo") }
        'path not starting with https://github.com/ fails';
