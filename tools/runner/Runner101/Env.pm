package Runner101::Env;
use Exporter qw(import);
@EXPORT_OK = qw(load_vars load_url load_path);

use strict;
use warnings;
use Cwd            qw( abs_path       );
use File::Path     qw(make_path       );
use File::Basename qw(basename dirname);
use URI::URL;
URI::URL::strict(1);


sub load_vars
{
    my ($vars) = @_;
    while (my ($key, $value) = each %$vars)
    {
        my $func   = $value =~ m{^[^:/]+://} ? \&load_url : \&load_path;
        $ENV{$key} = $func->($vars, $value);
    }
}


sub load_path
{
    my ($vars, $value) = @_;
    $value = "$vars->{$value->[0]}$value->[1]" if ref $value;

    my ($dir, $file) = $value =~ m{/$}
                     ? ($value,          ''                    )
                     : (dirname($value), '/' . basename($value));

    make_path($dir) if not -d $dir;
    my $path = abs_path "$dir$file";
    die "$dir$file is not a valid path" if length $path <= 1;
    $path
}


sub load_url
{
    my ($vars, $value) = @_;
    my $url = URI::URL->new($value);
    if ($url->scheme eq 'file')
    {   $url = URI::URL->newlocal(load_path($vars, $url->host . $url->path)) }
    "$url"
}


1
__END__

=head1 Runner101::Env

Module to load the runner's environment variables.

=head2 load_vars

    load_vars(\%vars)

Loads the environment variables given in the hashref C<$vars> into the actual
environment C<%ENV>. See the C<101worker/configs/env/README.md> for
documentation about how these variables should be defined.

Returns nothing useful and might die if L</load_path> or L</load_url> dies.

=head2 load_path

    load_path(\%vars, $value)

Turns a relative into an absolute path and, if necessary, creates its
directories. Returns the resulting absolute path with no trailing slashes.
Dies if the path is invalid.

If C<$value> does not end with a slash C</>, it is assumed to be a path to a
file and only the folders preceding it will be created. If it does end with a
slash, it is assumed to be a path to a directory and the full path will be
created as folders. Note that the resulting absolute path will have slashes
stripped though!

    load_path(\%vars, [$ref, $rest])

C<$value> may also be a tuple with the first element referencing another key
from C<$vars> and the second element being a path relative to that. The C<$ref>
is then loaded from C<$vars> and the result is joined with the C<$rest> before
proceeding. This only makes sense if C<$ref> references a directory.

=head2 load_url

    load_url(\%vars, $value)

Checks if C<$value> is a valid URL and returns it again. Dies on an invalid URL.

If the given C<$value> is a C<file://> URL, its content is first turned into an
absolute path through L</load_path>.

=cut
