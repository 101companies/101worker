use Test::Most      tests => 9;
use Cwd             qw(abs_path);
use File::Path      qw(make_path);
use File::Slurp     qw(write_file);
use File::Temp;
use Git::Repository;
use Repo101::Git    qw(git);
use Repo101::Pull;

my $test_dir = File::Temp->newdir;
my $repo_dir = "$test_dir/101repo";
my $pull     = Repo101::Pull->new(
    root_path => $repo_dir,
    deps_path => "$test_dir/gitdeps",
    root_url  => 'unused',
);


git('init', $repo_dir);
my $repo = Git::Repository->new(work_tree => $repo_dir);
write_file("$repo_dir/README", "Git doesn't like empty revisions.\n");
git($repo => 'add', "$repo_dir/README");
git($repo => qw(commit -m message));


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
