package Runner101::Changes;
use strict;
use warnings;
use File::Find;
use File::stat;


sub gather
{
    my ($time, $module) = @_;

    my $outpath = "$ENV{diffs101dir}/$time.$module.changes";
    open my $out, '>', $outpath or die "Can't write to $outpath: $!";

    find sub
    {
        my $file = $File::Find::name;
        return if not -f $file;

        my $stat = stat $file;
        if (!$stat)
        {
            warn "Can't stat $file: $!";
            return;
        }

        if    ($stat->mtime >= $time)
        {   print $out "m $file\n" }
        elsif ($stat->atime >= $time)
        {   print $out "a $file\n" }

    }, $ENV{results101dir}, $ENV{temps101dir}, $ENV{web101dir};
}


1
__END__

=head1 Runner101::Changes

Gather changes between module runs using the file system's atime (acces time)
and mtime (modification time) stamps for each file.

=head2 Note

On many Linux distributions, including Ubuntu, the default setting for atime
is called C<relatime>. This is an optimization to prevent writing to the disk
every time a file is accessed, and it will only update the atime if it isn't
already greater than the file's mtime.

This optimization breaks gathering dependencies and you need to turn it off to
use them properly. The setting you want is called C<strictatime>.

You can use the command C<sudo mount -o remount,strictatime /> (or replace the
C</> with whatever mount point your 101worker is on) to add the strictatime
option during runtime

Alternatively, you can edit your C</etc/fstab> and add the C<strictatime>
option to the appropriate mount point to make it permanent.

There is a test in F<t/11_changes.t> that will fail if you don't have
C<strictatime> enabled, so use that to check for it.

=head2 gather

    gather($time, $module)

Gathers changes that happened after the given C<$time> from the 101worker
result directories and writes them to
C<$ENV{diffs101dir}/$time.$module.changes>.

Walks through the folders defined by the environment variables
C<results101dir>, C<temps101dir> and C<web101dir> and looks at each file. If a
file has been modified after the given C<$time>, a line that looks like
C<m $filepath> is written into the output file. If the file has been accessed
after the given C<$time>, C<a $filepath> is written instead. If neither
occurred, nothing is written.

See the C<%.depend> target in F<101worker/Makefile> and the script in
F<101worker/tools/changes> for how to turn these changes files into graphs.

Also, read the L</Note>, it's important.

=cut
