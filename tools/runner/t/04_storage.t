use Test::Most      tests => 9;

use File::Slurp     qw(slurp);
use File::Temp      qw(tempdir);
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


throws_ok { store_diff("\0" => {}) } qr/Can't write to/,
          'storing to invalid file dies';

chmod 0, "$tempdir/full.diff" or die "Can't chmod full.diff: $!";
throws_ok { load_stored('full') } qr/Can't read from/,
          'loading from invalid file dies';

mkdir "$tempdir/dir.diff" or die "Can't mkdir dir.diff: $!";
throws_ok { remove_stored('dir') } qr/Can't unlink/,
          'removing invalid file dies';
