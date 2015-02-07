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


our %loaded;


sub load_vars
{
    my ($options) = @_;

    while (my ($key, $value) = each %$options)
    {   $loaded{$key} = $value if not ref $value }

    $ENV{$_} = load_var($options->{config}, $_) for keys %{$options->{config}};
}


sub load_var
{
    my ($config, $key) = @_;

    if (!exists $loaded{$key})
    {
        my $value     = $config->{$key};# // die "Missing key in config: $key";
        if (!defined $value) {
            use Data::Dumper;
            die "Missing $key\n" . Dumper($config);
        }
        my $func      = $value =~ m{^[^:/]+://} ? \&load_url : \&load_path;
        $loaded{$key} = $func->($config, $value);
    }

    $loaded{$key}
}


sub load_path
{
    my ($config, $value) = @_;
    $value =~ s/\$(\w+)/load_var($config, $1)/e while $value =~ /\$\w+/;

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
    my ($config, $value) = @_;
    my $url = URI::URL->new($value);
    if ($url->scheme eq 'file')
    {   $url = URI::URL->newlocal(load_path($config, $url->host . $url->path)) }
    "$url"
}


1
__END__

=head1 Runner101::Env

Module to load the runner's environment variables.

=head2 load_vars

    load_vars(\%vars)

Loads the environment variables given in the hashref C<$vars> into the actual
environment C<%ENV>. See the F<101worker/configs/env/README.md> for
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

If C<$value> contains the text I<$worker> or I<$result>, they are replaced with
the absolute paths to the local 101worker and result directory, respectively.

=head2 load_url

    load_url(\%vars, $value)

Checks if C<$value> is a valid URL and returns it again. Dies on an invalid URL.

If the given C<$value> is a C<file://> URL, its content is first turned into an
absolute path through L</load_path>.

=cut
