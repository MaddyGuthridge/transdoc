# Transdoc Python Handler

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

If the Python file contains syntax which cannot be parsed (by [libcst](https://libcst.readthedocs.io/en/latest/)),
a warning will be emitted, and the file will be transformed as plaintext.
