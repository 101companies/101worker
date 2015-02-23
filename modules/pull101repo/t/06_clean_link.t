use strict;
use warnings;
use Cwd        qw(abs_path);
use File::Path qw(make_path);
use Test::More tests => 9;
use Test::Exception;
use Repo101::Pull;

my $test_dir = abs_path('TEST') . "/clean_link$$";
my $repo_dir = "$test_dir/101repo";
my $pull     = Repo101::Pull->new(
    root_path => $repo_dir,
    deps_path => "$test_dir/gitdeps",
    root_url  => 'unused',
);

ok make_path("$repo_dir/dir/tree"),            'create directory tree';
ok symlink("$repo_dir/dir", "$repo_dir/link"), 'create link to tree';

is $pull->clean_link({}, 'tree'), undef, 'non-link is not cleaned';

is $pull->clean_link({"$repo_dir/link" => 'url'}, 'link'), undef,
   'existing member is not cleaned';

ok symlink("$repo_dir/nothing", "$repo_dir/bogus"), 'create bogus link';
throws_ok { $pull->clean_link({}, "$repo_dir/bogus") } qr{Couldn't resolve},
          'resolving bogus link fails';

lives_ok { $pull->clean_link({}, "$repo_dir/link") } 'cleaning link lives';
ok !-e "$repo_dir/link",                             'link was deleted';
ok !-e "$repo_dir/tree",                             'tree was deleted';
