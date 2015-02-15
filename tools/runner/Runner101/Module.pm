package Runner101::Module;
use strict;
use warnings;
use Try::Tiny;
use Runner101::Diff    qw(run_diff);
use Runner101::Helpers qw(slurp_json validate_json write_log);

use Class::Tiny qw(index name args dir log command
                   environment dependencies wantdiff);


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

    $self->command     ([split /\s+/, $json->{command} || '']);
    $self->environment ($json->{environment } // []);
    $self->dependencies($json->{dependencies} // []);
    $self->wantdiff    ($json->{wantdiff    }      );

    $parent->ensure_envs_exist  ($self);
    $parent->ensure_dependencies($self);
}


sub run
{
    my ($self, $parent) = @_;

    chdir $self->dir              or die "Couldn't cd into "  . $self->dir;
    open my $log, '>', $self->log or die "Couldn't write to " . $self->log;

    my $command = [qw(timeout -s KILL 1h), @{$self->command}, @{$self->args}];

    write_log($log, "${\$self->name}");
    write_log($log, 'directory : ', $self->dir);
    write_log($log, "command   : @$command");
    write_log($log, 'wantdiff  : ', $self->wantdiff, "\n");

    run_diff($command, $parent->diff, $log, $self->wantdiff)
}


1
