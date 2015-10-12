use Test::Most    tests => 4;
use Repo101::Pull;

# monkey-patch, because we don't actually care about git in this test
{
    no warnings 'redefine';
    my $pulls = 0;
    *Repo101::Pull::clone_or_pull = sub { ++$pulls };
}

my $pull = Repo101::Pull->new;

is $pull->pull_repo('path1', 'url1'), 1, 'new repo gets pulled';
is $pull->pull_repo('path1', 'url1'), 1, 'same repo again does nothing';
is $pull->pull_repo('path3', 'url1'), 1, 'even different path does nothing';
is $pull->pull_repo('path2', 'url2'), 2, 'different new repo gets pulled';
