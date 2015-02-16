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
    my ($config) = @_;
    $ENV{$_} = load_var($config, $_) for keys %$config;
}


sub load_var
{
    my ($config, $key) = @_;

    if (!exists $loaded{$key})
    {
        my $value     = $config->{$key} // die "Missing key in config: $key";
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

=head2 %loaded

    %Runner101::Env::loaded

Cache for already loaded variables.

=head2 load_vars

    load_vars(\%config)

Loads the environment variables given in C<$config> into the actual
environment C<%ENV>. See the F<101worker/configs/env/README.md> for
documentation about how these variables should be defined.

Returns nothing useful and might die if L<load_var>, L</load_path> or
L</load_url> dies.

=head2 load_var

    load_var(\%config, $key)

If L</%loaded> already contains the C<$key>, that value is returned.

Otherwise L</load_path> or L</load_url> is called, the result is cached in
L</%loaded> and then returned.

=head2 load_path

    load_path(\%config, $value)

Turns a relative into an absolute path and, if necessary, creates its
directories. Returns the resulting absolute path with no trailing slashes.
Dies if the path is invalid.

If C<$value> does not end with a slash C</>, it is assumed to be a path to a
file and only the folders preceding it will be created. If it does end with a
slash, it is assumed to be a path to a directory and the full path will be
created as folders. Note that the resulting absolute path will have slashes
stripped though!

All occurrences of C</\$\w+> (that is, variables like C<$output> or
C<$web101dir>) are replaced with the value they reference, obtained by calling
L</load_var>. Circular references will lead to infinite loops.

=head2 load_url

    load_url(\%config, $value)

Checks if C<$value> is a valid URL and returns it again. Dies on an invalid URL.

If the given C<$value> is a C<file://> URL, its content is first turned into an
absolute path through L</load_path>.

=cut
