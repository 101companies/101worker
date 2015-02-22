use File::Slurp     qw(slurp);
use File::Temp      qw(tempdir);
use Test::Most      tests => 7;
use Runner101::Diff qw(store_diff load_stored remove_stored);


my $tempdir       = tempdir;
$ENV{diffs101dir} = "$tempdir";


is_deeply load_stored('nonexistent'), {},
         'loading nonexistent file gives empty diff';

ok !remove_stored('nonexistent'), 'removing nonexistent file does nothing';


store_diff(empty => {});
is_deeply load_stored('empty'), {}, 'storing and loading empty diff';

ok -e "$tempdir/empty.diff",        'stored file remains';
ok remove_stored('empty') && !-e "$tempdir/empty.diff", 'removing stored file';


my $full = {qw(
    somefile          A
    somedir/file      M
    another/dir/asdf  D
    invalid/operation X
)};
store_diff(full => $full);
cmp_deeply load_stored('full'), $full,
         'storing and loading diff including invalid operation';


dies_ok { store_diff("\0" => {}) } 'storing to invalid file dies';
