use Capture::Tiny   qw(capture_stdout);
use Test::Most      tests => 9;
use Runner101::Diff qw(run_diff parse);


my $diffs = [];

is parse('',             $diffs), undef, 'Empty string is not parsed';
is parse('Some message', $diffs), undef, 'Regular message is not parsed';
is parse('123 W Street', $diffs), undef, 'Invalid operation is not parsed';
is_deeply                $diffs,  [],    'No diffs were gathered';


my @diff1 = ('A somefile', 'M someotherfile', 'D yetanotherfile');
my @diff2 = (@diff1, map { "$_.suffix" } @diff1);

my $testscript = q{
    /^\s*([AMD])\s+(.+?)\s*$/ or die;
    ++$i;
    print "got op: $1\n";
    print "$i - -\n";
    print "$i $1 $2.suffix\n";
};

my $output = capture_stdout
{
    is run_diff([qw(perl -ne), $testscript], \@diff1, \*STDOUT, 1), 0,
                'successful run returns exit code 0';
};

is_deeply \@diff1, \@diff2, 'diff result is correct';

is $output, "got op: A\ngot op: M\ngot op: D\n", 'other output is correct';


ok run_diff(['false'], [], \*STDOUT, 0), 'failing run returns non-zero';


dies_ok {
    local $SIG{__WARN__} = sub { die @_ };
    run_diff([], [], \*STDOUT, 1);
} 'invalid command causes warning';
