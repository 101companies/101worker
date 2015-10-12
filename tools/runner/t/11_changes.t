use Test::Most;
plan skip_all => 'irrelevant to production, set TEST101DEVEL environment '
               . 'variable to run it' unless $ENV{TEST101DEVEL};
plan tests    => 6;

use File::Temp         qw(tempdir);
use File::Slurp        qw(slurp write_file);
use Runner101::Changes;


my $dir = tempdir;
for (qw(diffs results temps web))
{
    my $subdir = "$dir/101$_";
    mkdir $subdir or BAIL_OUT "Couldn't mkdir $subdir: $!";
    $ENV{"${_}101dir"} = $subdir;
}


sub gather_ok
{
    my ($time, $name, $want, $message) = @_;
    Runner101::Changes::gather($time, $name);

    my $file = "$ENV{diffs101dir}/$time.$name.changes";
    my %have = map { chomp; reverse split /\s+/, $_, 2 } slurp $file;

    cmp_deeply \%have, $want, $message;

    sleep 1;
}


gather_ok time, empty => {}, 'no files gives empty changes file';


write_file "$ENV{results101dir}/file1" => 1;
write_file "$ENV{  temps101dir}/file2" => 2;
write_file "$ENV{    web101dir}/file3" => 3;

gather_ok time, first => {
              "$ENV{results101dir}/file1" => 'm',
              "$ENV{  temps101dir}/file2" => 'm',
              "$ENV{    web101dir}/file3" => 'm',
          }, 'initial modified files gives modifications';


slurp      "$ENV{results101dir}/file1";
slurp      "$ENV{  temps101dir}/file2";
mkdir      "$ENV{    web101dir}/dir";
write_file "$ENV{    web101dir}/dir/file4" => 4;

gather_ok time, second => {
              "$ENV{results101dir}/file1"     => 'a',
              "$ENV{  temps101dir}/file2"     => 'a',
              "$ENV{    web101dir}/dir/file4" => 'm',
          }, 'access and modification gives correct results';


slurp "$ENV{results101dir}/file1";
slurp "$ENV{  temps101dir}/file2";
slurp "$ENV{    web101dir}/file3";
slurp "$ENV{    web101dir}/dir/file4";

my $last = time;
gather_ok $last, atime => {
             "$ENV{results101dir}/file1"     => 'a',
             "$ENV{  temps101dir}/file2"     => 'a',
             "$ENV{    web101dir}/file3"     => 'a',
             "$ENV{    web101dir}/dir/file4" => 'a',
          }, 'access files again (will fail on relatime, see documentation!)';


chmod 0, "$ENV{diffs101dir}/$last.atime.changes";
throws_ok { Runner101::Changes::gather($last, 'atime') } qr/Can't write to/,
          'trying to write to invalid file dies';


{
    no warnings 'redefine'; # mock a stat failure
    *Runner101::Changes::stat = sub($) {};
}
my @expected = map { qr/Can't stat/ } 1 .. 4;

warnings_like { Runner101::Changes::gather(time, 'whatever') } \@expected,
              'failure to stat warns';
