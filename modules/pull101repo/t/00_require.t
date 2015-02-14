use strict;
use warnings;
use Test::More;

my @modules = qw(
    Class::Tiny
    File::Slurp
    Git::Repository
    LWP::Simple
    JSON
    Test::Most
    Try::Tiny
);

plan tests => scalar @modules;

for (@modules)
{
    require_ok $_ or BAIL_OUT "Couldn't load module: $_, please "
                            . "install it with ``cpan install $_''";
}
