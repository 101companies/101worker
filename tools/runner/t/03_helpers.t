use strict;
use warnings;
use Test::More         tests => 9;
use Test::Exception;
use Cwd                qw(abs_path);
use File::Slurp        qw(write_file);
use File::Temp;
use JSON;
use Runner101::Helpers qw(slurp_json guess_json validate_json);

my $path = File::Temp->newdir;

# slurp_json
write_file "$path/some.json", '{"a" : "b", "c" : ["d", "e"]}';
write_file "$path/not.json",  '123'; # valid JSON has to be object or array

is_deeply slurp_json("$path/some.json"), {a => 'b', c => [qw(d e)]},
                                            'slurp JSON file';
dies_ok { slurp_json("$path/not.json"   ) } 'slurp invalid JSON dies';
dies_ok { slurp_json("$path/nonexistent") } 'slurp nonexistent file dies';


# guess_json
write_file "$path/guess.json", '{"k" : "v"}';
is_deeply guess_json("$path/guess.json"), {k => 'v'}, 'guess JSON file path';
is_deeply guess_json('{"k" : "v"}'     ), {k => 'v'}, 'guess JSON string';
is_deeply guess_json( {k  => 'v'}      ), {k => 'v'}, 'guess JSON decoded';

$_ = {k => 'v'};
is_deeply guess_json, {k => 'v'}, 'guess JSON with implicit $_';


# validate_json
my $schema = {
    type        => 'array',
    items       => {type => 'string'},
    uniqueItems => JSON::true,
};

is_deeply validate_json([qw(a b c)], $schema), [qw(a b c)],
          'validating valid JSON against schema returns result';

dies_ok { validate_json([qw(a b b)], $schema) }
          'validating invalid JSON against schema dies';
