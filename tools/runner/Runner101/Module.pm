package Runner101::Module;
use strict;
use warnings;
use Try::Tiny;
use Runner101::Helpers qw(slurp_json validate_json);

use Class::Tiny qw(index name dir environment dependencies command);


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

    $self->environment ($json->{environment } // []);
    $self->dependencies($json->{dependencies} // []);

    $parent->ensure_envs_exist  ($self->environment);
    $parent->ensure_dependencies($self             );
}


sub execute
{
    my ($self) = @_;
    chdir $self->dir or die "Couldn't cd into " . $self->dir;
    system @{$self->command}
}


1
