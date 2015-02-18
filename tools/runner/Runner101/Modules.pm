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
    diff    => sub { {} },
};

use constant RUNNER_ENVS => qw(config101     config101schema module101schema
                               diffs101dir   logs101dir      output101dir
                               modules101dir worker101dir);


sub run
{
    my $self = __PACKAGE__->new(config => @_);

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

    Runner101::Env::load_vars($args->{config});
    $self->ensure_envs_exist(runner => RUNNER_ENVS);
    $self->die_if_invalid;

    my $names         = validate_json(@ENV{qw(config101 config101schema)});
    my $module_schema = slurp_json   ($ENV{module101schema});
    $self->names($names);

    for my $index (0 .. $#$names)
    {
        my $name = $names->[$index];
        push @{$self->modules}, Runner101::Module->new(
            index  => $index,
            name   => $name,
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

=head2 Attributes

None of these attributes are required in the constructor and you should
probably just let them use their default value.

=over

=item errors

Errors that have occured so far. See L</push_error> and L</die_if_invalid>.

=item names

The list of names of all modules to be ran.

=item modules

The list of C<Runner101::Module> objects of all modules to be ran.

=item diff

Aggregates the diff. The modules will fill this on their own when they are ran.

=back

=head2 run

    run(\%config)

Loads the given configuration (see F<101worker/configs/env>) into the
environment and validates that all necessary environment variables exist (see
L</RUNNER_ENVS>). Then loads the module list and validates it against its
schema.

If all that suceeded, it validates the C<module.json>s against their schema and
ensures that all dependencies and necessary environment variables are in order.

Finally, it runs each of the modules and gathers their diffs in-between.

Returns the resulting diff or dies with an error message if any of the
validation above failed.

=head3 Gathering Dependencies

If the environment variable C<runner101depend> is set, the runner will call
C<Runner101::Changes::gather> to collect which files have been accessed and
modified by each module. These changes are saved into the C<diffs101dir>
with filenames like C<$timestamp.$module.changes>.

See F<101worker/tools/depend> for a script that transforms those files into a
graph and the C<%.depend> target in the F<101worker/Makefile> for doing a
worker run with them and getting a PDF out of it in the end.

=head2 new

    Runner101::Modules->new( config => \%config )
    Runner101::Modules->new({config => \%config})

This instantiates a Runner101::Modules object and does the entire environment
and validation stuff described in L</run>. It doesn't run the modules though,
that's L</run>'s job.

Dies if any environment loading or validation fails.

=head2 push_error

    $self->push_error($type, $key, $value)

Adds the given value to C<< $self->errors >>list for the given C<$type> and
C<$key>.

For example, C<< $self->push_error('env', 'repo101dir', 'pull101repo') >>
would add an error message about the missing  environment variable
C<repo101dir> being required by the module C<pull101repo>.

See L</@ERROR_MESSAGES>, L</ensure_envs_exist> and L</ensure_dependencies>.

=head2 ensure_envs_exist

    $self->ensure_envs_exist($name, @envs)
    $self->ensure_envs_exist(Runner101::Module $module)

Ensures that all environment variables given in C<@envs> or
C<< $module->environment >> respectively actually exist in the environment. If
any are missing, appropriate errors are L</push_error>'d.

=head2 ensure_dependencies

    $self->ensure_dependencies(Runner101::Module $module)

Ensures that all dependencies on other modules in C<< $module->dependencies >>
are fulfilled. If any of the dependencies is missing or comes after C<$module>,
appropriate errors are L</push_error>'d.

=head2 @ERROR_MESSAGES

A mapping from error type to a printf format string. The format string receives
two arguments, the error key and value. See also L</push_error> and
L</die_if_invalid>.

=head2 die_if_invalid

    $self->die_if_invalid

Dies with a formatted error message if there's anything in
C<< $self->errors >>. Does nothing otherwise.

=cut
