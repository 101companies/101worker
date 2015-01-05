package Runner101::Modules;
use strict;
use warnings;
use File::Slurp        qw(slurp);
use List::MoreUtils    qw(first_index);
use List::Util         qw(pairmap);
use Proc::ChildError   qw(explain_child_error);
use Runner101::Helpers qw(slurp_json validate_json write_log);
use Runner101::Module;

use Class::Tiny {
    errors  => sub { {} },
    names   => sub { [] },
    modules => sub { [] },
    diff    => sub { [] },
};

use constant RUNNER_ENVS => qw(config101 config101schema module101schema);


sub run
{
    my $self = __PACKAGE__->new(@_);
    for (@{$self->modules})
    {
        my $prog      = 'Module ' . $_->name;
        write_log("Running $prog");

        my $exit_code = $_->run($self);

        write_log($exit_code
                ? explain_child_error({prog => $prog}, $exit_code, $!)
                : "$prog exited with code 0.");
    }
}


sub BUILD
{
    my ($self, $args) = @_;
    $self->ensure_envs_exist(runner => RUNNER_ENVS);
    $self->die_if_invalid;

    $self->names(validate_json(@ENV{qw(config101 config101schema)}));
    my $module_schema = slurp_json($ENV{module101schema});

    for (0 .. $#{$self->names})
    {
        my $name = $self->names->[$_];
        push @{$self->modules}, Repo101::Module->new(
            index  => $_,
            name   => $name,
            dir    => "$args->{modules_dir}/$name",
            parent => $self,
            schema => $module_schema,
        );
    }

    $self->die_if_invalid;
}


sub push_error
{
    my ($self, $type, $key, $value) = @_;
    push $self->errors->{$type}{$key} //= [], $value;
}


sub ensure_envs_exist
{
    my ($self, $name) = (shift, shift);
    for (ref $_[0] ? @{$_[0]} : @_)
    {   $self->push_error(env => $_, $name) if not exists $ENV{$_} }
}


sub ensure_dependencies
{
    my ($self, $module) = @_;
    for my $dep (@{$module->dependencies})
    {
        my $found = first_index { $_ eq $dep } @{$self->names};
        if ($found < 0)
        {   $self->push_error(missing => $dep, $module->name) }
        elsif ($found > $module->index)
        {   $self->push_error(late    => $dep, $module->name) }
    }
}


our @ERROR_MESSAGES = (
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
        map { sprintf $fmt => $_, join ', ', @{$msgs->{$_}} } keys %{$msgs}
    } @ERROR_MESSAGES;
}


1
