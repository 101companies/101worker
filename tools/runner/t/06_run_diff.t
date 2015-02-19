use Capture::Tiny     qw(capture_stdout);
use File::Temp        qw(tempdir);
use List::Util        qw(pairmap);
use Test::Most        tests => 12;
use Runner101::Diff   qw(run_diff parse);
use Runner101::Module;


my $tempdir       = tempdir;
$ENV{diffs101dir} = "$tempdir";
my $stored        = "$ENV{diffs101dir}/test.diff";
{ open my $out, '>', $stored or die "Can't touch $stored: $!"; }


my $diffs = {};

is parse('',             $diffs), undef, 'Empty string is not parsed';
is parse('Some message', $diffs), undef, 'Regular message is not parsed';
is parse('123 W Street', $diffs), undef, 'Invalid operation is not parsed';
is_deeply                $diffs,  {},    'No diffs were gathered';


my %diff1 = (
    somefile       => 'A',
    someotherfile  => 'M',
    yetanotherfile => 'D',
);
my %diff2 = (%diff1, pairmap { ("$a.suffix" => $b) } %diff1);


my $testscript = q{
    /^\s*([AMD])\s+(.+?)\s*$/ or die;
    ++$i;
    print "got op: $1\n";
    print "$i - -\n";
    print "$i $1 $2.suffix\n";
};

my $module = bless {
    name     => 'test',
    command  => [qw(perl -ne), $testscript],
    wantdiff => 1,
} => 'Runner101::Module';


ok -e $stored, "stored diff exists";

my $output = capture_stdout
{
    is run_diff($module, \%diff1, \*STDOUT), 0,
                'successful run returns exit code 0';
};

is_deeply \%diff1, \%diff2, 'diff result is correct';

ok $output =~ /^got op: A$/m && $output =~ /^got op: M$/m
   && $output =~ /^got op: D$/m, 'other output is correct';

ok !-e $stored, "stored diff is deleted on success";


$module->command(['false']);
ok run_diff($module, {}, \*STDOUT), 'failing run returns non-zero';
ok -e $stored, "diff is stored on failure";


$module->command([]);
dies_ok {
    local $SIG{__WARN__} = sub { die @_ };
    run_diff($module, {}, \*STDOUT);
} 'invalid command causes warning';
