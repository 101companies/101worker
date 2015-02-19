use File::Temp         qw(tempdir);
use File::Slurp        qw(slurp);
use Test::Most;
use Runner101::Changes;

if ($ENV{TEST101CHANGES})
{   plan tests => 1 }
else
{   plan skip_all => 'irrelevant to production, set TEST101CHANGES to run it' }


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
    my $have = slurp "$ENV{diffs101dir}/$time.$name.changes";
    eq_or_diff $have, $want, $message;
}


gather_ok(time, 'test', '', 'no files gives empty changes file');
