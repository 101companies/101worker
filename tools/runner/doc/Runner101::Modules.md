# Runner101::Modules

A class for instantiating, validating and running a set of modules. From the
outside, you probably just want to call ["run"](#run).

## Attributes

None of these attributes are required in the constructor and you should
probably just let them use their default value.

- errors

    Errors that have occured so far. See ["push\_error"](#push_error) and ["die\_if\_invalid"](#die_if_invalid).

- names

    The list of names of all modules to be ran.

- modules

    The list of `Runner101::Module` objects of all modules to be ran.

- diff

    Aggregates the diff. The modules will fill this on their own when they are ran.

## run

    run(\%config)

Loads the given configuration (see `101worker/configs/env`) into the
environment and validates that all necessary environment variables exist (see
["RUNNER\_ENVS"](#runner_envs)). Then loads the module list and validates it against its
schema.

If all that suceeded, it validates the `module.json`s against their schema and
ensures that all dependencies and necessary environment variables are in order.

Then it runs each of the modules and gathers their diffs in-between and saves

Returns the resulting diff or dies with an error message if any of the
validation above failed.

### Gathering Dependencies

If the environment variable `runner101depend` is set, the runner will call
`Runner101::Changes::gather` to collect which files have been accessed and
modified by each module. These changes are saved into the `diffs101dir`
with filenames like `$timestamp.$module.changes`.

See `101worker/tools/depend` for a script that transforms those files into a
graph and the `%.depend` target in the `101worker/Makefile` for doing a
worker run with them and getting a PDF out of it in the end.

## BUILD

    Runner101::Modules->new( config => \%config )
    Runner101::Modules->new({config => \%config})

This instantiates a Runner101::Modules object and does the entire environment
and validation stuff described in ["run"](#run). It doesn't run the modules though,
that's ["run"](#run)'s job.

Dies if any environment loading or validation fails.

## push\_error

    $self->push_error($type, $key, $value)

Adds the given value to `$self->errors`list for the given `$type` and
`$key`.

For example, `$self->push_error('env', 'repo101dir', 'pull101repo')`
would add an error message about the missing  environment variable
`repo101dir` being required by the module `pull101repo`.

See ["@ERROR\_MESSAGES"](#error_messages), ["ensure\_envs\_exist"](#ensure_envs_exist) and ["ensure\_dependencies"](#ensure_dependencies).

## ensure\_envs\_exist

    $self->ensure_envs_exist($name, @envs)
    $self->ensure_envs_exist(Runner101::Module $module)

Ensures that all environment variables given in `@envs` or
`$module->environment` respectively actually exist in the environment. If
any are missing, appropriate errors are ["push\_error"](#push_error)'d.

## ensure\_dependencies

    $self->ensure_dependencies(Runner101::Module $module)

Ensures that all dependencies on other modules in `$module->dependencies`
are fulfilled. If any of the dependencies is missing or comes after `$module`,
appropriate errors are ["push\_error"](#push_error)'d.

## @ERROR\_MESSAGES

A mapping from error type to a printf format string. The format string receives
two arguments, the error key and value. See also ["push\_error"](#push_error) and
["die\_if\_invalid"](#die_if_invalid).

## die\_if\_invalid

    $self->die_if_invalid

Dies with a formatted error message if there's anything in
`$self->errors`. Does nothing otherwise.
