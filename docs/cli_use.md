# Using the Transdoc CLI

Transdoc can be accessed using a CLI with the `transdoc` command.

```bash
$ transdoc --version
transdoc, version 1.2.0
```

## Rule file

You must specify a Python file containing the Transdoc rules you wish to use
while transforming your documentation using the `-r` flag.

```bash
$ transdoc -r path/to/rules.py
...
```

## Input files

You must specify an input file or directory as the primary argument.

```bash
$ transdoc input.txt -r path/to/rules.py
...
```

If `-` is given as an input path, input will be read from `stdin`.

## Output files

By using the `-o` flag, you can specify your intended output file/directory.

```bash
$ transdoc input.txt -o output.txt -r path/to/rules.py
...
```

If `-` is given as an output path, output will be written to `stdout`.
Otherwise, you must specify an output path or give the `--dryrun` flag.

## Other options

* `--dryrun`: don't produce any output file(s). Just check for errors in the
  inputs. This still evaluates all rules, so any side effects of rule
  evaluation will still occur.
* `--force`: always overwrite the output file/directory, regardless of whether
  it contains data.
* `--skip-if`: skip over files that match the given regular expression.
* `-v`, `-vv`, `-vvv`: control verbosity of logging.
* `--help`: show help information
* `--version`: show version information

### Additional notes

You cannot disable the pride flags in the `--help` output by using the
`NO_PRIDE` environment variable.
