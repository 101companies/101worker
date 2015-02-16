package Runner101::Modules;
use strict;
use warnings;
use File::Slurp         qw(slurp);
use List::MoreUtils     qw(first_index);
use List::Util          qw(pairmap);
use POSIX               qw(strftime);
use Proc::ChildError    qw(explain_child_error);
use Try::Tiny;
use Runner101::Changes;
use Runner101::Env;
use Runner101::Helpers  qw(slurp_json validate_json write_log);
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
        my $prog = $_->name;
        write_log("running $prog");

        my $start     = time;
        my $exit_code = $_->run($self);
        my $taken     = time - $start;

        my $time   = strftime('%H:%M:%S', gmtime $taken);
        my $reason = $exit_code
                   ? explain_child_error({prog => $prog}, $exit_code, $!)
                   : "$prog exited with value 0";

        write_log("$reason after $time");

        if ($ENV{runner101depend})
        {
            write_log("gathering changes for $prog");
            try
            {   Runner101::Changes::gather($start, $prog) }
            catch
            {   warn $_ };
            sleep 1;
        }
    }
    $self->diff
}


sub BUILD
{
    my ($self, $args) = @_;

    Runner101::Env::load_vars($args);
    $self->ensure_envs_exist(runner => RUNNER_ENVS);
    $self->die_if_invalid;

    my $config        = validate_json(@ENV{qw(config101 config101schema)});
    my $module_schema = slurp_json   ($ENV{module101schema});

    my (@names, @args);
    for (@$config)
    {
        my ($name, @rest) = split;
        push @names, $name;
        push @args, \@rest;
    }
    $self->names(\@names);

    for my $index (0 .. $#names)
    {
        my $name = $names[$index];
        push @{$self->modules}, Runner101::Module->new(
            index  => $index,
            name   => $name,
            args   => $args[$index],
            dir    => "$ENV{modules101dir}/$name",
            log    => "$ENV{   logs101dir}/$name.log",
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
    my ($self, $module) = (shift, shift);
    my ($name, $envs  ) = ref $module
                        ? ($module->name, $module->environment)
                        : ($module,       \@_                 );
    for (@$envs)
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

    die join "\n - ", "Validation errors:", @{$errors->{other} || []}, pairmap
    {
        my ($msgs, $fmt) = ($errors->{$a}, $b);
        map { sprintf $fmt => $_, join ', ', @{$msgs->{$_}} } keys %{$msgs}
    } @ERROR_MESSAGES;
}


1
__END__

=head1 Runner101::Modules

A class for instantiating, validating and running a set of modules. From the
outside, you probably just want to call L</run>.

=head2 run

    run(
        config => \%config,
        
    )

=back

=cut
