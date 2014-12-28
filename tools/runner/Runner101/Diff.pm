package Runner101::Diff;
use Exporter qw(import);
@EXPORT_OK = qw(run_diff parse);

use strict;
use warnings;
use IPC::Run qw();


sub parse
{
    my ($line, $diffs) = @_;

    if    ($line =~ /^\s*(\d+)\s+([AMD])\s+(.+?)\s*$/)
    {
        push @$diffs, "$2 $3";
        $1
    }
    elsif ($line =~ /^\s*(\d+)\s+-\s+-\s*$/)
    {   $1    }
    else
    {   undef }
}


sub run_diff
{
    my ($command, $diffs) = @_;

    my $in = join "\n", @$diffs;
    my $out;
    IPC::Run::run($command, \$in, \$out) or die "Error running @$command: $!";

    parse($_, $diffs) // print $_, "\n" for split /\n/, $out;
}
