use strict;
use warnings;
use Cwd        qw(abs_path);
use File::Temp;
use Test::More tests => 6;
use Test::Exception;
use Repo101::Pull;

my $test_dir = File::Temp->newdir;
my $pull     = Repo101::Pull->new(
    root_path => 'unused',
    deps_path => 'unused',
    root_url  => 'unused',
);

ok mkdir("$test_dir/src"), 'create source dir';

lives_ok { $pull->symlink("$test_dir/src", "$test_dir/dst") } 'symlink to dir';

lives_ok { $pull->symlink("$test_dir/src", "$test_dir/dst") } 'delete and link';

throws_ok { $pull->symlink("$test_dir/nonexistent", "$test_dir/bogus") }
          qr{Not a directory}, 'linking to nonexistent directory fails';

ok mkdir("$test_dir/notalink"), 'create incorrect link dir';
throws_ok { $pull->symlink("$test_dir/src", "$test_dir/notalink") }
          qr{Couldn't link}, 'trying to unlink a real folder fails';
