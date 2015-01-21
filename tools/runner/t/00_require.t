use strict;
use warnings;
use Test::More;

my @modules = qw(
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

plan tests => scalar @modules;

for (@modules)
{
    require_ok $_ or BAIL_OUT "Couldn't load module: $_, please "
                            . "install it with ``cpan install $_''";
}
