use strict;
use warnings;
use Test::More    tests => 3;
use Repo101::Pull;


# monkey-patch, because we don't actually care about git in this test
{
    no warnings 'redefine';
    my $pulls = 0;
    *Repo101::Pull::clone_or_pull = sub { ++$pulls };
}

my $pull = Repo101::Pull->new;

is $pull->pull_repo('unused', 'url1'), 1, 'new repo gets pulled';
is $pull->pull_repo('unused', 'url1'), 1, 'same repo again does nothing';
is $pull->pull_repo('unused', 'url2'), 2, 'different new repo gets pulled';
