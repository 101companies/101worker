use Test::Most      tests => 7;
use Test::Exception;
use Repo101::Pull;

my $root_path = '/test/101repo';
my $deps_path = '/test/gitdeps';
my $pull      = Repo101::Pull->new(
    root_path => $root_path,
    deps_path => $deps_path,
    root_url  => 'unused',
);

sub check_diffs(@)
{
    my ($message, $remaining, $expected) = (pop, pop, pop);
    is_deeply $pull->merge_diffs(@_), $expected, "$message (result)";
    is_deeply $_[0], $remaining, "$message (remaining)"
}


check_diffs {}, {}, {}, 'empty diffs';

check_diffs {
                "$root_path/file"        => 'A',
                "$root_path/folder/file" => 'M',
            }, {
                'file'                   => 'A',
                'folder/file'            => 'M',
            }, {}, 'simple root diff';

check_diffs {
                "$root_path/file"        => 'D',
                "$root_path/folder/file" => 'D',
                "$root_path/other"       => 'A',
                "$deps_path/file"        => 'A',
                "$deps_path/folder/file" => 'M',
            }, "$deps_path/folder", 'dep/folder', {
                'file'                   => 'A',
                'folder/file'            => 'M',
                'dep/folder/file'        => 'M',
            }, {
                "$root_path/file"        => 'D',
                "$root_path/folder/file" => 'D',
                "$root_path/other"       => 'A',
                "$deps_path/file"        => 'A',
            }, 'path matching and rewriting';

throws_ok { $pull->merge_diffs({"$root_path/file" => 'D'}) }
          qr/Already got a diff entry for file/,
          'duplicate diff entry fails';
