package Runner101::Module;
use strict;
use warnings;
use Try::Tiny;
use Runner101::Diff    qw(run_diff);
use Runner101::Helpers qw(slurp_json validate_json);

use Class::Tiny qw(index name dir environment dependencies);

our $SIGNAL  = 'KILL';
our $TIMEOUT = '1h';


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

    $self->environment ($json->{environment } // []  );
    $self->dependencies($json->{dependencies} // []  );

    $parent->ensure_envs_exist  ($self->environment);
    $parent->ensure_dependencies($self             );
}


sub run
{
    my ($self, $parent) = @_;
    chdir $self->dir or die "Couldn't cd into " . $self->dir;
    run_diff(['timeout', '-s', $SIGNAL, $TIMEOUT, 'make'], $parent->diff)
}


1
