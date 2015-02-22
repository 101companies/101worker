use Test::Most;
plan skip_all => 'irrelevant to production, set TEST101DEVEL environment '
               . 'variable to run it' unless $ENV{TEST101DEVEL};


eval 'use Test::Pod::Coverage';
plan skip_all => 'this requires the Test::Pod::Coverage module' if $@;


my @modules = all_modules('Runner101');
plan tests => scalar @modules;


my $trustme = {trustme => [qr/^BUILD$/]};
pod_coverage_ok($_, $trustme, $_) for map { "Runner101::$_" } @modules;
