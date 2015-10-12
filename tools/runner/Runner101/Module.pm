package Runner101::Module;
use strict;
use warnings;
use Try::Tiny;
use Runner101::Diff    qw(run_diff);
use Runner101::Helpers qw(slurp_json validate_json write_log);

use Class::Tiny qw(index name dir log environment dependencies
                   command wantdiff metadependencies metaobtained);


our @PREFIX = qw(timeout -s KILL 1h);


sub BUILD
{
    my ($self, $args) = @_;
    my  $parent       = $args->{parent};

    my $json = try
    {
        validate_json($self->dir . '/module.json', $args->{schema})
    }
    catch
    {
        push @{$parent->errors->{other}}, $_;
        {}
    };

    $self->command([@PREFIX, split /\s+/, $json->{command} || '']);
    $self->environment ($json->{environment } // []);
    $self->dependencies($json->{dependencies} // []);
    $self->wantdiff($json->{wantdiff});

    $self->metadependencies($json->{metadata}->{dependencies} // []);
    $self->metaobtained($json->{metadata}->{obtained} // []);

    $parent->ensure_envs_exist      ($self);
    $parent->ensure_metadependencies($self);
    $parent->ensure_dependencies    ($self);
}


sub run
{
    my ($self, $parent) = @_;

    chdir $self->dir or die "Couldn't cd into "  . $self->dir;

    my $log;
    if ($ENV{DEBUG101})
    {   $log = \*STDERR }
    else
    {   open $log, '>', $self->log or die "Couldn't write to " . $self->log }

    run_diff($self, $parent->diff, $log)
}


1
__END__

=head1 Runner101::Module

Class that represents a worker module to be run.

=head2 Attributes

The following attributes are required to be passed in the constructor:

=over

=item index

Where this module appears in the list of modules to be run. The first module
has index 0.

=item name

The name of this module, should be the same as its folder name.

=item dir

The absolute path to the module's directory. There must be a F<module.json> in
this directory. When the module is ran, the current directory is changed to
this path.

=item log

The name of the log file to write to. If the file already exists, its contents
are clobbered. The folder the file is supposed to be in needs to exist too.

=back

These other attributes are loaded from the F<module.json> when the object is
constructed:

=over

=item command

The command to run the module, as an arrayref. This is the same as the
C<command> entry in the F<module.json>, except the string is split by
whitespace so that it can be passed without shell interpolation.

=item wantdiff

If this module wants to receive a diff on its stdin or not.

=item environment

A list of environment variables required by the module.

=item dependencies

A list of other modules this module depends on.

=item metadependencies

TODO: document

=item metaobtained

TODO: document

=back

=head2 BUILD

    Runner101::Module->new(
        parent => Runner101::Modules $parent,
        schema => $module_json_schema,
        index  => $module_index,
        name   => $module_name,
        dir    => $path_to_module_dir,
        log    => $path_to_log_file,
    )

Construct a module object. This will attempt to load this module's
F<module.json> that should be in the given C<dir>. Its contents are validated
against the given C<schema> and saved as this module's L</Attributes>.

Then the required environment variables and dependencies of the Modules 
and the Metadata are validated by the given C<parent>,
using C<< $parent->ensure_envs_exist >> for the enviorment,
C<< $parent-ensure_metadependencies >> for the Meta-Dependencies and
C<< $parent->ensure_dependencies >> for the Module-Dependencies.

If anything goes wrong during all this, the parent will die with the
appropriate error messages.

=head2 run

    $self->run(Runner101::Modules $parent)

Changes the current working directory to C<< $self->diff >> and runs
C<< $self->command >>. The command will be run using C<timeout>, which will
kill the subprocess after one hour. Output of the command is written to the
file whose path is specified by C<< $self->log >>.

Modifieds C<< $parent->diff >> in-place and returns the exit code of the
command run. Dies if the working directory couldn't be changed or the log file
couldn't be written to.

See also C<Runner101::Diff>.

=cut
