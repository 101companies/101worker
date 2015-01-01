package Runner101::Modules;
use strict;
use warnings;
use File::Slurp        qw(slurp);
use List::MoreUtils    qw(first_index);
use List::Utils        qw(pairmap);
use Runner101::Helpers qw(slurp_json validate_json);
use Runner101::Module;

use Class::Tiny {
    errors  => sub { {} },
    names   => sub { [] },
    modules => sub { [] },
};

use constant RUNNER_ENVS => qw(config101 config101schema module101schema);


sub run
{
    ...
}


sub BUILD
{
    my ($self, $args) = @_;
    $self->ensure_envs_exist(runner => RUNNER_ENVS);
    $self->die_if_invalid;

    $self->names(validate_json(@ENV{qw(config101 config101schema)}));
    my $module_schema = slurp_json($ENV{module101schema});

    for (my $i = 0; $i < @{$self->names}; ++$i)
    {
        my $name = $self->names->[$i];
        Repo101::Module->new(
            index  => $i,
            name   => $name,
            dir    => "$args->{modules_dir}/$name",
            parent => $self,
            schema => $module_schema,
        )
    }

    $self->die_if_invalid;
}


sub ensure_envs_exist
{
    my ($self, $name) = (shift, shift);
    for (ref $_[0] ? @{$_[0]} : @_)
    {
        if (!exists $ENV{$_})
        {
            $self->errors->{env}{$_} //= [];
            push @{$self->errors->{env}{$_}}, $name;
        }
    }
}


sub ensure_dependencies
{
    my ($self, $module) = @_;
    for my $dep (@{$module->dependencies})
    {
        my $found = first_index { $_ eq $dep } @{$self->names};
        if ($found < 0)
        {
            $self->errors->{missing}{$dep} //= [];
            push @{$self->errors->{missing}{$dep}}, $module->name;
        }
        elsif ($found > $module->index)
        {
            $self->errors->{late}{$_} //= [];
            push @{$self->errors->{late}{$dep}}, $module->name;
        }
    }
}


use constant ERROR_MESSAGES => (
    env     => 'Missing environment variable %s required by %s',
    missing => 'Module %s required before %s, but is missing',
    late    => 'Module %s required before %s, but appears after instead',
);

sub die_if_invalid
{
    my ($self) = @_;
    my $errors = $self->errors;
    return if not %$errors;

    die join "\n - ", "Validation errors:", @{$errors->{other}}, pairmap
    {
        my ($msgs, $fmt) = ($errors->{$a}, $b);
        map { sprintf $fmt => $_, join ', ', $msgs->{$_} } keys %{$msgs}
    } ERROR_MESSAGES;
}


1
