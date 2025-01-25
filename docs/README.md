# 🏳️‍⚧️ Transdoc 🏳️‍⚧️

A simple transformation system for documentation, where Python functions are
used to add to documentation.

## Installation

`pip install transdoc`

To install handlers for Python, run `pip install transdoc[python]` instead.

## Usage

### Rule functions

Rules are defined using simple Python functions that return strings.

```py
# rules.py
def my_rule() -> str:
    '''
    A simple rule for rewriting docstrings
    '''
    return "This text was added by Transdoc!"
```

Rules can take arbitrary arguments.

```py
# rules.py
def repeat(text: str, n: int = 2) -> str:
    '''
    Repeat the given text any number of times.
    '''
    return " ".join([text] * n)
```

```py
def mdn_link(e: str) -> str:
    '''
    Return a Markdown-formatted link to the MDN Web Docs for the given HTML
    element.
    '''
    return (
        f"[`<{e}>`]"
        f"(https://developer.mozilla.org/en-US/docs/Web/HTML/Element/{e})"
    )
```

### Calling rule functions

Any text placed within `{{` double-braces `}}` is treated as a call to a rule
function.

```txt
Hello world!
{{my_rule}}
```

Transforming this input will produce the following output.

```txt
Hello world!
This text was added by Transdoc!
```

Rule functions can be called using Python-like syntax.

```py
{{repeat('Hi!', n=3)}}
```

```txt
Hi! Hi! Hi!
```

Since passing a single string as an argument is so common, Transdoc adds a
special syntax for this. Simply place the string argument in square brackets.

```md
In HTML, links can be created using the anchor
({{mdn_link[a]}}) element.
```

```md
In HTML, links can be created using the anchor
([`<a>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a)) element.
```

### Transforming documentation in source code

Transdoc can also be used to transform documentation in source, by using a
handler for your desired language. For more information, see the page on [handlers](handlers.md).
