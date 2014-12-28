use strict;
use warnings;
use Test::More tests => 6;

for (qw(File::Slurp IPC::Run JSON JSON::Schema Test::Exception URI::URL))
{
    require_ok $_ or BAIL_OUT "Couldn't load module: $_, please "
                            . "install it with ``cpan install $_''";
}
