package Runner101::Diff;
use Exporter qw(import);
@EXPORT_OK = qw(merge_diffs parse store_diff load_stored
                remove_stored build_diff run_diff);

use strict;
use warnings;
use List::Util         qw(pairmap);
use IPC::Run           qw();
use Try::Tiny;
use Runner101::Helpers qw(write_log);


our %merge_resolution = (
    'AM' => 'A',
    'AD' =>  '',
    'MM' => 'M',
    'MD' => 'D',
    'DA' => 'M',
    'AA' => 'A', # from here the cases don't really make sense, but we'll
    'MA' => 'M', # handle them anyway so that the end result looks right
    'DM' => 'M',
    'DD' => 'D',
);

sub merge_diff
{
    my ($diff, $op, $file) = @_;
    return $diff->{$file} = $op if not exists $diff->{$file};

    my $key      = "$diff->{$file}$op";
    my $resolved = $merge_resolution{$key} // die "Can't resolve $key";

    if ($resolved)
    {   $diff->{$file} = $resolved }
    else
    {   delete $diff->{$file}      }

    $resolved
}


sub merge_diffs
{
    my ($old, $new) = @_;

    my $merged = {%$old};
    while (my ($file, $op) = each %$new)
    {   merge_diff($merged, $op, $file) }

    $merged
}


sub parse
{
    my ($line, $diff) = @_;

    if ($line =~ /^\s*(\d+)\s+([AMD])\s+(.+?)\s*$/)
    {
        merge_diff($diff, $2, $3);
        $1
    }
    elsif ($line =~ /^\s*(\d+)\s+-\s+-\s*$/)
    {   $1    }
    else
    {   undef }
}


sub store_diff
{
    my ($name, $diff) = @_;

    my $path = "$ENV{diffs101dir}/$name.diff";
    open my $out, '>', $path or die "Can't write to $path: $!";

    while (my ($file, $op) = each %$diff)
    {   print $out "$op $file\n" }
}


sub load_stored
{
    my ($name) = @_;
    my  $path  = "$ENV{diffs101dir}/$name.diff";
    my  $diff  = {};

    if (-e $path)
    {
        open my $in, '<', $path or die "Can't read from $path: $!";
        while (<$in>)
        {
            chomp;
            my ($op, $path) = split /\s+/, $_, 2;
            $diff->{$path}  = $op;
        }
    }

    $diff
}


sub remove_stored
{
    my ($name) = @_;
    my  $path  = "$ENV{diffs101dir}/$name.diff";
    if (-e $path)
    {   unlink $path or die "Can't unlink $path: $!" }
}


sub build_diff
{
    my ($module, $current, $log) = @_;
    return {} if not $module->wantdiff;

    my $recovery = load_stored($module->name);
    if (%$recovery)
    {
        write_log($log, 'recovering stored diff');
        my $last_result = load_stored('result');
        merge_diffs(merge_diffs($recovery, $last_result), $current)
    }
    else
    {   $current }
}


sub run_diff
{
    my ($module, $diff, $log) = @_;

    my $input_diff = build_diff($module, $diff, $log);

    my $out;
    my $exit_code = do {
        local $?;
        local $SIG{PIPE} = 'IGNORE';

        my $in = join "\n", pairmap { "$b $a" } %$input_diff;
        try
        {   IPC::Run::run($module->command, \$in, \$out, $log) }
        catch
        {   warn $_ };

        $?
    };

    if ($module->wantdiff && $exit_code)
    {   store_diff($module->name, $input_diff) }
    else
    {   remove_stored($module->name)           }

    print $log "\n";

    for (split /^/, $out)
    {
        next unless /\S/; # skip empty lines
        my $lines = parse($_, $diff);
        print $log $_ if not defined $lines;
    }

    $exit_code
}


1
__END__

=head1 Runner101::Diff

Contains functions to handle the diff protocol between the runner and modules.

=head2 Diff Protocol

The diff protocol is a simple line-based protocol.

See F<101worker/libraries/incremental101> for a Python library for this
protocol, use that instead of writing a new implementation.

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

=head2 merge_diff

    merge_diff($diff, $op, $file)

Merges the given C<$file> and C<$op>eration into the given C<$diff>. If the
C<$file> isn't yet in C<$diff>, it will just be inserted. Otherwise, the
result will be chosen so that the end result reflects the actual state of
the file system, according to the following table:

    $diff $op $resolved
      A    M      A
      A    D
      M    M      M
      M    D      D
      D    A      M
      A    A      A
      M    A      M
      D    M      M
      D    D      D

Returns the operation that the merge resolved to. Dies if a set of operations
can't be resolved, which should only happen if there's an invalid operation
present that isn't C<A>, C<M> or C<D>.

=head2 merge_diffs

    merge_diffs($old, $new)

Merges two entire diffs and returns the merged diff. None of the input values
are modified.

See L</merge_diff> about how individual operations are resolved.

=head2 parse

    parse($line, \@diffs)

Attempts to parse C<$line> as a diff. If there's anything interesting in it,
it will be pushed to the C<$diffs> arrayref. Returns the I<lines read so far>
if it could parse the line and C<undef> otherwise.

=head2 store_diff

    store_diff($name, $diff)

Stores the given C<$diff> in a file called C<$ENV{diffs101dir}/$name.diff>.
Any existing file of that name will be clobbered.

Returns nothing useful and dies if the file can't be written to.

See also L</load_stored> and L</remove_stored>.

=head2 load_stored

    load_stored($name)

Attempts to load a diff that was previously stored with the same C<$name> via
L</store_diff>.

Returns the loaded diff or an empty diff if there was no file to load anything
from. Dies if the file exists, but can't be read.

See also L</store_diff> and L</remove_stored>.

=head2 remove_stored

    remove_stored($name)

Attempts to removes a diff file that was previously stored with the same
C<$name> via L</store_diff>.

Returns true if there was a file and it was deleted, or false if there was no
file to be deleted. Dies if the file exists, but can't be deleted.

See also L</store_diff> and L</load_stored>.

=head2 build_diff

    build_diff($module, $current, $log)

Builds a diff for the given C<$module>.

If it doesn't want a diff, an empty diff is returned.

If it does want a diff and there is a previously stored diff (see
L</store_diff>), it is recovered (see L</load_stored> and merged with the
result diff from the previous run and the given C<$current> diff (see
L</merge_diffs>). The fact that this happened is logged to C<$log>. The
resulting diff is returned.

Otherwise, if there is no stored diff to be recovered, it returns the given
C<$current> diff.

=head2 run_diff

    run_diff(Runner101::Module $module, $diff, $log)

Builds a diff for the given C<$module>, as per L</build_diff>. Then runs the
C<$module>'s command.

After the command ran, its output is L</parse>d for diff output (even if
C<< $module->wantdiff >> is false!) and any diffs found are added to the given
C<$diff>.

Any other output is appended to the given C<$log> filehandle. Note that this
means that the log will contain all stderr first and then all stdout.

If the C<$module> takes a diff as input and the command exited with a non-zero
status, the diff is stored via L</store_diff>. Otherwise, any stored diff that
might have existed is removed via C</remove_diff>.

Returns the exit code of the process run and warns on errors like broken pipe.

=cut
