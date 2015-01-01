use strict;
use warnings;
use Test::More tests => 8;

for (qw(File::Slurp IPC::Run JSON JSON::Schema List::MoreUtils
        Test::Exception Try::Tiny URI::URL))
{
    require_ok $_ or BAIL_OUT "Couldn't load module: $_, please "
                            . "install it with ``cpan install $_''";
}
