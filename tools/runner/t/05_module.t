use strict;
use warnings;
use File::Temp;
use Test::More         tests => 3;
use Runner101::Helpers qw(slurp_json spew_json);
use Runner101::Module;
use Runner101::Modules;
use constant MODULE  => 'Runner101::Module';
use constant MODULES => 'Runner101::Modules';

my $schema = slurp_json('../../../101worker/schemas/module.schema.json');
my $parent = bless {} => MODULES;
my $dir    = File::Temp->newdir;

my $args   = {
    index  => 0,
    name   => 'module0',
    dir    => $dir,
    parent => $parent,
    schema => $schema,
};


$parent->errors({});
Runner101::Module->new($args);

cmp_ok scalar @{$parent->errors->{other}}, '==', 1,
      'Missing module file causes error';


$parent->errors({});
spew_json("$dir/module.json", {});
Runner101::Module->new($args);

cmp_ok scalar @{$parent->errors->{other}}, '==', 1,
      'Invalid module file causes error';


$parent->errors({});
spew_json("$dir/module.json", {dependencies => [], environment => []});
Runner101::Module->new($args);

ok !exists $parent->errors->{other}, 'Valid module file causes no error';
