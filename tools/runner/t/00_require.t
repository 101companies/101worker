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
);

plan tests => 1 + scalar @modules;

for (@modules)
{
    require_ok $_ or BAIL_OUT "Couldn't load module: $_, please "
                            . "install it with ``cpan install $_''";
}

cmp_ok system('timeout'), '!=', -1, 'timeout command is available' or diag $!;
