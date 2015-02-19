use Test::Most         tests => 7;
use Class::Tiny;
use List::Util         qw(pairmap);
use Runner101::Modules;
use constant MODULE  => 'Runner101::Module';
use constant MODULES => 'Runner101::Modules';


# Circumvent BUILD method
my @def = %{Class::Tiny->get_all_attribute_defaults_for(MODULES)};

sub new
{
    my $self = bless {} => MODULES;
    for (0 .. 5)
    {
        my $module = {
            index        => $_,
            name         => "module$_",
            dependencies => [],
        };
        push @{$self->names  }, $module->{name};
        push @{$self->modules}, bless $module => MODULE;
    }
    $self
}

my $self;


# ensure_envs_exist
$self = new;
$ENV{"env$_"} = $_ for 1 .. 3;

$self->ensure_envs_exist(test1 => qw(env1 env2 env3));
is_deeply $self->errors, {}, 'ensure existing envs';

$self->ensure_envs_exist(test2 => qw(env3 env4 env5));
$self->ensure_envs_exist(test3 => qw(env1 env5 env6));
is_deeply $self->errors, {env => {
                              env4 => ['test2'         ],
                              env5 => ['test2', 'test3'],
                              env6 => [         'test3'],
                         }}, 'ensure missing envs causes errors';

# ensure_dependencies
$self = new;
$self->ensure_dependencies($self->modules->[0]);
is_deeply $self->errors, {}, 'empty dependencies';

$self->modules->[3]->dependencies([qw(module0 module1 module2)]);
$self->ensure_dependencies($self->modules->[3]);
is_deeply $self->errors, {}, 'valid dependencies';

$self->modules->[1]->dependencies([qw(module0 module1 module2 nonexistent)]);
$self->ensure_dependencies($self->modules->[1]);
is_deeply $self->errors, {
              late    => {module2     => ['module1']},
              missing => {nonexistent => ['module1']},
          }, 'invalid dependencies lead to correct errors';


# die_if_invalid
$self = new;

lives_ok { $self->die_if_invalid } 'no errors live';

$self->errors({
    other   => ['Some error message', 'Another error message'],
    env     => {somevar => [qw(module1 module2)]             },
    missing => {module1 => [qw(module2 module3)]             },
    late    => {module2 => [qw(module3 module4)]             },
});

my %messages  = @Runner101::Modules::ERROR_MESSAGES;
my $e_env     = sprintf $messages{env    } => 'somevar', 'module1, module2';
my $e_missing = sprintf $messages{missing} => 'module1', 'module2, module3';
my $e_late    = sprintf $messages{late   } => 'module2', 'module3, module4';

my $regex = quotemeta "Validation errors:\n"
                    . " - Some error message\n"
                    . " - Another error message\n"
                    . " - $e_env\n"
                    . " - $e_missing\n"
                    . " - $e_late";

throws_ok { $self->die_if_invalid } qr/$regex/,
         'errors die with correct diagnostic message';
