# Contributing to Transdoc

I'd love to have your contributions!

## Development setup

This project uses [`uv`](https://docs.astral.sh/uv/) as a package manager.

Install dependencies

```sh
# Generally, you won't want to install the `python` group, as it breaks the test
# suite. Tests for that are found over in the transdoc-python repo.
uv sync --group ci --group docs
```

Run linting

```sh
uv run ruff check
```

Run test suite

```sh
uv run pytest
```

Run type-checking

```sh
uv run mypy
```

Build package

```sh
uv build
```
