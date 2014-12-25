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
    my ($hash) = @_;
    while (my ($key, $value) = each %$hash)
    {
        my $func   = $value =~ m{^[^:/]+://} ? \&load_url : \&load_path;
        $ENV{$key} = $func->($hash, $value);
    }
}


sub load_url
{
    my ($hash, $value) = @_;
    my $url = URI::URL->new($value);
    if ($url->scheme eq 'file')
    {   $url = URI::URL->newlocal(load_path($hash, $url->host . $url->path)) }
    "$url"
}


sub load_path
{
    my ($hash, $value) = @_;

    if (ref $value)
    {
        my $file = $value->[-1];
        my @dirs = map { $hash->{$_} } @$value[0 .. @$value - 2];
        $value   = join '/', @dirs, $file;
    }

    my ($dir, $file) = $value !~ m{/$}
                     ? (dirname($value), '/' . basename($value))
                     : ($value,          ''                    );

    make_path($dir) if not -d $dir;
    my $path = abs_path "$dir$file";
    die "$dir$file is not a valid path" if length $path <= 1;
    $path
}


1
__END__
