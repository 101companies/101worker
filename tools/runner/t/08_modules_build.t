use Test::Most         tests => 8;

use Cwd                qw(getcwd);
use File::Slurp        qw(slurp write_file);
use File::Temp         qw(tempdir);
use JSON;
use Runner101::Module;
use Runner101::Modules;

$ENV{diffs101dir} = '.'; # to silence some warnings

my $tempdir = tempdir;
my $config  = "$tempdir/config.json";
{
    no warnings qw(once redefine); # monkey-patch
    *Runner101::Module::new = sub
    {
        my %args = (@_[1 .. $#_]);

        if ($args{name} eq 'fail')
        {   $args{parent}->push_error(qw(env something fail)) }

        $args{parent} = "$args{parent}"; # for identity
        \%args
    };
}


throws_ok { Runner101::Modules->new } qr/required by runner/,
          'missing runner environment variables dies';


my %args = (
    config => {
        config101       => $config,
        config101schema => '../../schemas/config.schema.json',
        module101schema => '../../schemas/module.schema.json',
    },
);
for (Runner101::Modules::RUNNER_ENVS)
{   $args{config}{$_} = $_ if not exists $args{config}{$_} }


throws_ok { Runner101::Modules->new(%args) } qr{\Q$config\E},
          'missing config file to be loaded dies';


write_file $config => encode_json [qw(module0 module1 fail module2)];
throws_ok { Runner101::Modules->new(%args) }
          qr{Missing environment variable something required by fail},
          'any module validation failure dies';


my $names = [map { "module$_" } 0 .. 2];
write_file $config => encode_json $names;

lives_ok
{
    my $m = Runner101::Modules->new(%args);
    is_deeply $m->names, $names, 'module names are loaded from config';

    my $cwd    = getcwd;
    my $schema = decode_json scalar slurp $args{config}{module101schema};
    for (0 .. 2)
    {
        is_deeply $m->modules->[$_], {
            index  => $_,
            name   => "module$_",
            dir    => "$cwd/modules101dir/module$_",
            log    => "$cwd/logs101dir/module$_.log",
            parent => "$m",
            schema => $schema,
        }, 'module constructor called with correct arguments';
    }
} 'everything validates fine';
