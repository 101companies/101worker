use Test::Most        tests => 4;

use Runner101::Diff   qw(build_diff);
use Runner101::Module;


my $module = bless {name => 'module'} => 'Runner101::Module';
my %stored;
{
    no warnings 'redefine'; # monkey-patch
    *Runner101::Diff::load_stored = sub { $stored{$_[0]} || {} };
}


my $current = {};
sub test_build_diff($$)
{
    my ($want, $message) = @_;
    is_deeply build_diff($module, $current, \*STDOUT), $want, $message;
}


$module->wantdiff(0);
test_build_diff {}, 'module not wanting a diff gives empty diff';


$current = {qw(
    file1 A
    file2 M
    file3 D
)};
$module->wantdiff(1);
test_build_diff $current, 'no stored diff gives current diff';


$stored{module} = {qw(
    file1 D
    file2 M
    file3 A
    file4 D
)};
test_build_diff {qw(
                    file1 M
                    file2 M
                    file4 D
                )}, 'stored diff but no result merges current and stored';


$stored{result} = {qw(
    file1 A
    file2 M
    file5 A
)};
test_build_diff {qw(
                    file1 M
                    file2 M
                    file4 D
                    file5 A
                )}, 'stored diff and result merges current, stored and result';
