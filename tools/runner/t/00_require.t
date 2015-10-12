use strict;
use warnings;
use Test::More;

my @modules = qw(
    Capture::Tiny
    File::Slurp
    IPC::Run
    JSON
    JSON::Schema
    List::MoreUtils
    Proc::ChildError
    Test::Most
    Try::Tiny
    URI::URL
    YAML
);

plan tests => 1 + scalar @modules;

for (@modules)
{
    require_ok $_ or BAIL_OUT "Couldn't load module: $_, please "
                            . "run sudo make install";
}


my $ret = system qw(timeout -s KILL 1 sleep 3);
if ($ret == -1)
{   fail "timeout command is not available: $!" }
else
{   cmp_ok $ret & 127, '==', 9, 'timeout command works correctly' }
