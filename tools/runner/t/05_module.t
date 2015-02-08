use Test::Most         tests => 7;
use File::Temp;
use Runner101::Helpers qw(slurp_json spew_json);
use Runner101::Module;
use Runner101::Modules;
use constant MODULE  => 'Runner101::Module';
use constant MODULES => 'Runner101::Modules';

my $schema = slurp_json('../../../101worker/schemas/module.schema.json');
my $parent = bless {} => MODULES;
my $dir    = File::Temp->newdir;
my $buf    = '';

my $args   = {
    index    => 0,
    name     => 'module0',
    args     => [],
    dir      => $dir,
    parent   => $parent,
    schema   => $schema,
    log      => \$buf,
    wantdiff => 1,
};


$parent->errors({});
Runner101::Module->new($args);

cmp_ok scalar @{$parent->errors->{other}}, '==', 1,
      'missing module file causes error';


$parent->errors({});
spew_json("$dir/module.json", {});
Runner101::Module->new($args);

cmp_ok scalar @{$parent->errors->{other}}, '==', 1,
      'invalid module file causes error';


$parent->errors({});
spew_json("$dir/module.json", {
              command      => 'python program.py',
              wantdiff     => 1,
              dependencies => [],
              environment  => [],
          });

my $module = Runner101::Module->new($args);
is_deeply $module->command, [qw(python program.py)],
          'command gets split by whitespace';

ok !exists $parent->errors->{other}, 'valid module file causes no error';


# monkey-patch, because we don't test run_diff here
{
    no warnings 'redefine';
    *Runner101::Module::run_diff = sub { [@_[0, 1, 3]] };
}

is_deeply $module->run($parent),
          [[qw(timeout -s KILL 1h python program.py)], [], 1],
          'running module calls run_diff with correct arguments';

$module->log('/');
throws_ok { $module->run($parent) } qr/Couldn't write to/,
          'invalid log target dies';

$module->dir('\\');
throws_ok { $module->run($parent) } qr/Couldn't cd into/,
          'invalid directory dies';

chdir;
