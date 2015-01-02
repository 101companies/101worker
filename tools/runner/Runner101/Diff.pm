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

    my $out;
    my $in = join "\n", @$diffs;
    IPC::Run::run($command, \$in, \$out);

    parse($_, $diffs) // print $_, "\n" for split /\n/, $out;

    $? # child process exit code
}


1
__END__

=head1 Runner101::Diff

Contains functions to handle the diff protocol between the runner and modules.

=head2 Diff Protocol

The diff protocol is a simple line-based protocol.

See F<101worker/libraries/incremental> for a Python library for this protocol,
use that instead of writing a new implementation.

=head3 Output From Module

The modules output the diff lines to their stdout. Any line that the runner
can't parse will be ignored and printed instead, because a lot of worker
modules are very wordy.

Each line has the following elements, separated by whitespace:

=over

=item lines read so far

The number of lines of diff that the module has read. Should be used for error
recovery sometime.

=item operation

What has been done to the file. This may be C<A> for an added file, C<M> for a
modified file and C<D> for a deleted file.

=item file path

The path to the file. Shall be an absolute path.

=back

Operation and file path may I<both> be a single hyphen C<->, in case the module
just wants to tell the runner how many input lines it has read so far.

=head3 Input To Module

The modules receive the diff lines to their stdin. Any line that a module can't
parse should cause the module to fail, because the runner isn't supposed to
output garbage.

Each line has the following elements, separated by whitespace, which work the
same way as above:

=over

=item operation

=item file path

=back

=head2 parse

    parse($line, \@diffs)

Attempts to parse C<$line> as a diff. If there's anything interesting in it,
it will be pushed to the C<$diffs> arrayref. Returns the I<lines read so far>
if it could parse the line and C<undef> otherwise.

=head2 run_diff

    run_diff(\@command, \@diffs)

Executes the given C<$command>, which is an arrayref containing the arguments
of the command. The given C<$diffs> goes into the stdin and the output gets
L</parse>d. Returns the exit code of the C<$command> run.

=cut
