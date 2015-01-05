use strict;
use warnings;
use Test::More tests => 9;

for (qw(File::Slurp IPC::Run JSON JSON::Schema List::MoreUtils
        Proc::ChildError Test::Exception Try::Tiny URI::URL))
{
    require_ok $_ or BAIL_OUT "Couldn't load module: $_, please "
                            . "install it with ``cpan install $_''";
}
