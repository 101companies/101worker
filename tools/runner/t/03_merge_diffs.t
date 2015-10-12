use Test::Most      tests => 5;

use File::Temp      qw(tempdir);
use Runner101::Diff qw(merge_diffs);


my $full = {qw(
    file1           A
    file2           M
    file3           D
    somedir/file4   A
    somedir/file5   M
    somedir/file6   D
    otherdir/file7  A
    otherdir/file8  M
    otherdir/file9  D
)};


is_deeply merge_diffs({}, {}), {},
         'merge empty diff with empty diff gives empty diff';
is_deeply merge_diffs($full, {}), $full,
         'merge full diff with empty diff gives full diff';
is_deeply merge_diffs({}, $full), $full,
         'merge empty diff with full diff gives full diff';


throws_ok { merge_diffs($full, {file1 => 'X'}) } qr/Can't resolve AX/,
           'merging invalid diff operation dies';


is_deeply merge_diffs({qw(
              oldA  A
              oldM  M
              oldD  D
              AA    A
              AM    A
              AD    A
              MA    M
              MM    M
              MD    M
              DA    D
              DM    D
              DD    D
          )},
          {qw(
              newA  A
              newM  M
              newD  D
              AA    A
              AM    M
              AD    D
              MA    A
              MM    M
              MD    D
              DA    A
              DM    M
              DD    D
          )}),
          {qw(
              oldA  A
              oldM  M
              oldD  D
              newA  A
              newM  M
              newD  D
              AA    A
              AM    A
              MA    M
              MM    M
              MD    D
              DA    M
              DM    M
              DD    D
          )},
          'merging diffs gives correct end result';
