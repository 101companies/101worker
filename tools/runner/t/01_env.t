use Test::Most      tests => 23;

use Cwd             qw(abs_path);
use File::Temp;
use Runner101::Env  qw(load_vars load_url load_path);


my $tmpdir = File::Temp->newdir;
my $olddir = abs_path;
chdir "$tmpdir" or die "Could not cd into $tmpdir: $!";
my $pwd    = abs_path;


my %hash = (
    output101dir  => "$tmpdir/output",
    results101    => '101results/',
    repo101       => '101results/101repo/',
    dumps101      => '101web/dumps/',
    views101      => '101web/views/',
    config101     => '101worker/configs/file',
    rules101dump  => '$dumps101/rules.json',
    repo101url    => 'https://github.com/101repo',
    data101url    => 'http://data.101companies.org/',
    gitdeps101url => 'file://101results/gitdepsrc/',
    dir101        => '$output101dir/somedir/',
    ref101        => '$dir101/somefile',
);


sub check_path($$)
{
    my ($key, $message) = @_;
    my $path = $hash{$key};
    $path =~ s{/$}{};
    is load_path(\%hash, $hash{$key}), "$pwd/$path", "load $message";
    ok -d "$pwd/$path",                              "create $message";
}

check_path results101 => 'single folder';
check_path repo101    => 'existing folder';
check_path views101   => 'multiple folders';


is load_path(\%hash, $hash{'config101'}), "$pwd/101worker/configs/file",
                                      'load dirs and file';
ok  -d "$pwd/101worker/configs",      'dirs are created';
ok !-e "$pwd/101worker/configs/file", 'but file is not';


is load_path(\%hash, $hash{'rules101dump'}), "$pwd/101web/dumps/rules.json",
                                       'load path with references';
ok  -d "$pwd/101web/dumps",            'create path with references';
ok !-e "$pwd/101web/dumps/rules.json", 'only folders are created';


my @depth = $pwd =~ m{/}g;  # make a path like ../../../../../
my $bogus = '../' x @depth; # that goes all the way to the root
dies_ok { load_path({}, $bogus) } 'bogus path dies';
dies_ok { load_path({}, "\0?/") } 'invalid path dies';


is load_path(\%hash, $hash{ref101}), "$tmpdir/output/somedir/somefile",
   'load path with $variable';
ok -d "$tmpdir/output/somedir", 'path with $variable is created';


dies_ok { load_path(\%hash, '$nonexistent/asdf') }
       'nonexistent $variable dies';


is load_url(\%hash, $hash{'repo101url'}), 'https://github.com/101repo',
  'load https URL';
is load_url(\%hash, $hash{'data101url'}), 'http://data.101companies.org/',
  'load http URL';
is load_url(\%hash, $hash{'gitdeps101url'}), "file://$pwd/101results/gitdepsrc",
  'load local path as URL';

dies_ok { load_url({}, 'C:\Documents and Settings') } 'invalid URL dies';


%Runner101::Env::loaded = ();

load_vars(\%hash);
my %given    = map { ($_ => $ENV{$_}) } keys %hash;

my %expected = (
    output101dir  => "$tmpdir/output",
    results101    => "$pwd/101results",
    dumps101      => "$pwd/101web/dumps",
    views101      => "$pwd/101web/views",
    repo101       => "$pwd/101results/101repo",
    config101     => "$pwd/101worker/configs/file",
    rules101dump  => "$pwd/101web/dumps/rules.json",
    repo101url    => 'https://github.com/101repo',
    data101url    => 'http://data.101companies.org/',
    gitdeps101url => "file://$pwd/101results/gitdepsrc",
    dir101        => "$tmpdir/output/somedir",
    ref101        => "$tmpdir/output/somedir/somefile"
);

is_deeply \%given, \%expected, 'load variables into environment';


chdir $olddir;


%Runner101::Env::loaded = ();
throws_ok {
    local $SIG{__WARN__} = sub { die @_ };
    load_vars({
        circular  => '$reference',
        reference => '$circular',
    });
} qr/Deep recursion/, 'circular references lead to infinite loops';
