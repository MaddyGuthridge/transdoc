# Transdoc Handlers

Transdoc uses Python's [entrypoints specification](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#using-package-metadata)
to discover and use Transdoc handler plugins.

## Handler responsibilities

Handler plugins should perform the following functions:

* Inform Transdoc of the file extensions they can handle.
* When given a file, load it and apply transformations using Transdoc's API.

## Adding your library as a transdoc handler

In your `pyproject.toml`, include the following:

```toml
[project.entry-points.'transdoc.handlers']
plugin_name = 'plugin_module_name:entrypoint'
```

## Module contents

The `entrypoint` object should have a number of methods, such that it matches
the `TransdocHandler` protocol.

::: transdoc.TransdocHandler
