use Test::Most    tests => 11;
use Capture::Tiny qw(capture_merged);
use List::Util    qw(pairs);

BEGIN
{
    # mock out time and sleep to make them predicatable
    my $time      = 0;
    my $more_time = sub { ++$time };
    *CORE::GLOBAL::time = *CORE::GLOBAL::sleep = $more_time;
}
use Runner101::Changes;
use Runner101::Module;
use Runner101::Modules;


my @modules = map { bless {name => "module$_"} => 'Runner101::Module' } 1 .. 3;
{
    no warnings qw(once redefine); # more mocks
    *Runner101::Changes::gather = sub
    {
        my (undef, $prog) = @_;
        die 'mock' if $prog eq 'module3';
    };

    *Runner101::Module::run = sub { 0 };

    *Runner101::Modules::store_diff = sub {};

    *Runner101::Modules::new = sub
    {   bless {modules => \@modules} => 'Runner101::Modules' };
}


delete $ENV{runner101depend};
my $output;
lives_ok { $output = capture_merged { Runner101::Modules::run } }
         'run without gathering changes';

for (pairs 1 .. 6)
{
    my ($start, $end) = @$_;
    my  $module       = int($end / 2);
    like $output, qr/^report:\tmodule$module\t0\t[^\t]+\t$start\t$end$/m,
         "...report for module $module";
}
like   $output, qr/report-ok\n$/s, '...last log line is report-ok';
unlike $output, qr/gathering changes/, '...no changes are gathered';


$ENV{runner101depend} = 1;
lives_ok { $output = capture_merged { Runner101::Modules::run } }
         'run and gather changes';

like $output, qr/report-ok\n$/s, '...last log line is report-ok';

my @changes = $output =~ /gathering changes/g;
cmp_ok @changes, '==', 3, '...changes for all modules are gathered';
like $output, qr/^mock/m, '...errors from gather are logged';


{
    no warnings qw(redefine);
    *Runner101::Module::run  = sub { die 'mock' };
}
throws_ok { Runner101::Modules::run } qr/mock/,
          'runner dies if module execution dies';
