use strict;
use warnings;
use Test::More tests => 6;

for (qw(Class::Tiny File::Slurp Git::Repository LWP::Simple JSON
        Test::Exception))
{
    require_ok $_ or BAIL_OUT "Couldn't load module: $_, please "
                            . "install it with ``cpan install $_''";
}
