package Runner101::Changes;
use strict;
use warnings;
use File::Find;
use File::stat;


sub gather
{
    my ($time, $module) = @_;

    my $outpath = "$ENV{diffs101dir}/$time.$module.changes";
    open my $out, '>', $outpath or die "Can't open $outpath: $!";

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
