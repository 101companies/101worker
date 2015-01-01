use strict;
use warnings;
use Test::More      tests => 19;
use Test::Exception;
use Cwd             qw(abs_path);
use Runner101::Env  qw(load_vars load_url load_path);


mkdir 'TEST'       or die "Could not mkdir TEST: $!" if not -d 'TEST';
mkdir "TEST/env$$" or die "Could not mkdir TEST/env$$: $!";
chdir "TEST/env$$" or die "Could not cd into TEST/env$$: $!";
my $pwd = abs_path;


my %hash = (
    results101    => '101results/',
    repo101       => '101results/101repo/',
    dumps101      => '101web/dumps/',
    views101      => '101web/views/',
    config101     => '101worker/configs/file',
    rulesDump101  => [qw(dumps101 rules.json)],
    repo101url    => 'https://github.com/101repo',
    data101url    => 'http://data.101companies.org/',
    gitdeps101url => 'file://101results/gitdepsrc/',
);


# load_path
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

is load_path(\%hash, $hash{'rulesDump101'}), "$pwd/101web/dumps/rules.json",
                                       'load path with references';
ok  -d "$pwd/101web/dumps",            'create path with references';
ok !-e "$pwd/101web/dumps/rules.json", 'only folders are created';

my @depth = $pwd =~ m{/}g;  # make a path like ../../../../../
my $bogus = '../' x @depth; # that goes all the way to the root
dies_ok { load_path({}, $bogus) } 'bogus path dies';
dies_ok { load_path({}, "\0?/") } 'invalid path dies';


# load_url
is load_url(\%hash, $hash{'repo101url'}), 'https://github.com/101repo',
  'load https URL';
is load_url(\%hash, $hash{'data101url'}), 'http://data.101companies.org/',
  'load http URL';
is load_url(\%hash, $hash{'gitdeps101url'}), "file://$pwd/101results/gitdepsrc",
  'load local path as URL';

dies_ok { load_url({}, 'C:\Documents and Settings') } 'invalid URL dies';


# load_vars
load_vars(\%hash);
my %given    = map { ($_ => $ENV{$_}) } keys %hash;
my %expected = (
    results101    => "$pwd/101results",
    dumps101      => "$pwd/101web/dumps",
    views101      => "$pwd/101web/views",
    repo101       => "$pwd/101results/101repo",
    config101     => "$pwd/101worker/configs/file",
    rulesDump101  => "$pwd/101web/dumps/rules.json",
    repo101url    => 'https://github.com/101repo',
    data101url    => 'http://data.101companies.org/',
    gitdeps101url => "file://$pwd/101results/gitdepsrc",
);
is_deeply \%given, \%expected, 'load variables into environment';
