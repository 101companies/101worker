use Test::Most         tests => 13;

use Capture::Tiny      qw(capture);
use Cwd                qw(abs_path);
use File::Slurp        qw(write_file);
use File::Temp;
use JSON;
use Runner101::Helpers qw(slurp_json spew_json guess_json
                          validate_json write_log);

my $path = File::Temp->newdir;
my $json = {a => 'b', c => [qw(d e)]};


# slurp_json
write_file "$path/some.json", encode_json($json);
write_file "$path/not.json", '123'; # valid JSON has to be object or array

is_deeply slurp_json("$path/some.json"), $json, 'slurp JSON file';
dies_ok { slurp_json("$path/not.json"   ) }     'slurp invalid JSON dies';
dies_ok { slurp_json("$path/nonexistent") }     'slurp nonexistent file dies';


# spew_json
spew_json("$path/spew.json", $json);
is_deeply slurp_json("$path/spew.json"), $json, 'spew JSON file';

dies_ok { spew_json("$path/no.json", 123) }     'spew invalid JSON dies';


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


# write_log
my $buf = '';
open my $out, '>', \$buf;
write_log($out, 'hello', ' ', 'world!');
like $buf, qr/^\[.+\] hello world!\n$/s, 'write log to filehandle';

my $stdout = capture { write_log('another hello to everyone!') };
like $stdout, qr/^\[.+\] another hello to everyone!\n$/s, 'write log to stdout';
