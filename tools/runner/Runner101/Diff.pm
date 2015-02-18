package Runner101::Diff;
use Exporter qw(import);
@EXPORT_OK = qw(store_diff run_diff parse);

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
    'DA' => 'A',
    'AA' => 'A', # from here the cases don't really make sense, but we'll
    'MA' => 'M', # handle them anyway so that the end result looks right
    'DM' => 'A',
    'DD' => 'D',
);

sub merge_diff
{
    my ($diff, $op, $file) = @_;
    return $diff->{$file} = $op if not exists $diff->{$file};

    my $key      = "$diff->{$file}$op";
    my $resolved = $merge_resolution{$key} // die "Can't resolve $key";

    if ($resolved)
    {   $diff->{$file} = $op  }
    else
    {   delete $diff->{$file} }

    $resolved
}


sub merge_diffs
{
    my ($old, $new) = @_;

    my  $merged     = {%$old};
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
        parse($_, $diff) while <$in>;
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

=head2 parse

    parse($line, \@diffs)

Attempts to parse C<$line> as a diff. If there's anything interesting in it,
it will be pushed to the C<$diffs> arrayref. Returns the I<lines read so far>
if it could parse the line and C<undef> otherwise.

=head2 run_diff

    run_diff(\@command, \@diffs, $log, $wantdiff)

Executes the given C<$command>, which is an arrayref containing the arguments
of the command. If C<$wantdiff> is true, the given C<$diffs> are piped into
it. The stdandard error of the command goes into the givnen C<$log> filehandle.

After the command ran, its output is L</parse>d for diff output (even if
C<$wantdiff> is false!) and any diffs found are added to the given C<$diffs>.
Any other output is appended to the given C<$log> filehandle. Note that this
means that the log will contain all stderr first and then all stdout.

Returns the exit code of the process run and warns on errors like broken pipe.

=cut
