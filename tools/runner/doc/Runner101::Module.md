# Runner101::Module

Class that represents a worker module to be run.

## Attributes

The following attributes are required to be passed in the constructor:

- index

    Where this module appears in the list of modules to be run. The first module
    has index 0.

- name

    The name of this module, should be the same as its folder name.

- dir

    The absolute path to the module's directory. There must be a `module.json` in
    this directory. When the module is ran, the current directory is changed to
    this path.

- log

    The name of the log file to write to. If the file already exists, its contents
    are clobbered. The folder the file is supposed to be in needs to exist too.

These other attributes are loaded from the `module.json` when the object is
constructed:

- command

    The command to run the module, as an arrayref. This is the same as the
    `command` entry in the `module.json`, except the string is split by
    whitespace so that it can be passed without shell interpolation.

- wantdiff

    If this module wants to receive a diff on its stdin or not.

- environment

    A list of environment variables required by the module.

- dependencies

    A list of other modules this module depends on.

## BUILD

    Runner101::Module->new(
        parent => Runner101::Modules $parent,
        schema => $module_json_schema,
        index  => $module_index,
        name   => $module_name,
        dir    => $path_to_module_dir,
        log    => $path_to_log_file,
    )

Construct a module object. This will attempt to load this module's
`module.json` that should be in the given `dir`. Its contents are validated
against the given `schema` and saved as this module's ["Attributes"](#attributes).

Then the required environment variables and dependencies are validated by the
given `parent`, using `$parent->ensure_envs_exist` and
`$parent->ensure_dependencies`.

If anything goes wrong during all this, the parent will die with the
appropriate error messages.

## run

    $self->run(Runner101::Modules $parent)

Changes the current working directory to `$self->diff` and runs
`$self->command`. The command will be run using `timeout`, which will
kill the subprocess after one hour. Output of the command is written to the
file whose path is specified by `$self->log`.

Modifieds `$parent->diff` in-place and returns the exit code of the
command run. Dies if the working directory couldn't be changed or the log file
couldn't be written to.

See also `Runner101::Diff`.
