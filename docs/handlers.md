# Transdoc handlers

Out-of-the-box, Transdoc can only process text in plain-text files (eg `.txt`,
`.md`).

## Python

```sh
pip install transdoc[python]
```

A handler for docstrings within Python. Python code is kept as-is, with only
triple-quote strings being modified.

```py
# Input
def example():
    """
    An example function.

    {{my_rule}}
    """
```

```py
# Output
def example():
    """
    An example function.

    This text was added by Transdoc!
    """
```

## HTML

A handler for HTML documentation.

* I haven't written this yet.
* Intended to process text within HTML, without affecting other content such
  as CSS and JS.
