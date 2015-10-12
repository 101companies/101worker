use Test::Most      tests => 21;
use Cwd             qw(abs_path);
use File::Compare;
use File::Slurp     qw(write_file append_file);
use File::Temp;
use List::Util      qw(pairs);
use Scalar::Util    qw(blessed);
use Repo101::Git    qw(clone_or_pull git);

my   $test_dir = File::Temp->newdir;
my  $local_dir = "$test_dir/local";
my $remote_dir = "$test_dir/remote";
my  $clone_dir = "$test_dir/clone";


sub run_git # helper to test a bunch of git commands in a row
{
    my $repo = blessed $_[0] ? shift : undef;
    for (pairs @_)
    {
        my ($message, $commands) = @$_;
        lives_ok { git($repo || (), @$commands) } $message;
    }
}


run_git(
    'git init local repo'  => ['init',           $local_dir ],
    'git init remote repo' => ['init', '--bare', $remote_dir],
);
my  $local = Git::Repository->new(work_tree =>  $local_dir);
my $remote = Git::Repository->new(work_tree => $remote_dir);


my @files = qw(test1 test2 test3);
write_file("$local_dir/$_", map { "$_\n" } $_, @files) for @files;

run_git($local,
    'add test files'  => [qw(add) => @files                   ],
    'commit files'    => [qw(commit -qm initial)              ],
    'add origin'      => [qw(remote add origin) => $remote_dir],
    'push test files' => [qw(push -qu origin master)          ],
);

is_deeply clone_or_pull($clone_dir, $remote_dir), {
              "$clone_dir/test1" => 'A',
              "$clone_dir/test2" => 'A',
              "$clone_dir/test3" => 'A',
          }, 'clone';

is compare("$clone_dir/$_", "$local_dir/$_"), 0, "$_ identical" for @files;


is_deeply clone_or_pull($clone_dir, $remote_dir), {}, 'empty pull';


append_file("$local_dir/test1", "asdf\n");
write_file ("$local_dir/test4", "public static void main(String[] args)\n");
$files[1] = 'test4';

run_git($local,
    'modify test1'         => [qw(add test1)          ],
    'remove test2'         => [qw(rm  test2)          ],
    'add test4'            => [qw(add test4)          ],
    'commit modifications' => [qw(commit -qm modified)],
    'push modifications'   => [qw(push -q)            ],
);

is_deeply clone_or_pull($clone_dir, $remote_dir), {
              "$clone_dir/test1" => 'M',
              "$clone_dir/test2" => 'D',
              "$clone_dir/test4" => 'A',
          }, 'pull';

ok !-e "$clone_dir/test2", 'test2 really removed';

is compare("$clone_dir/$_", "$local_dir/$_"), 0, "$_ identical" for @files;
