# Recipes

Common usage patterns with Transdoc.

## Skip gitignored files

```py
from pathlib import Path

import transdoc
import git  # gitpython library

# Rules file
from . import transdoc_rules


transformer = transdoc.TransdocTransformer.from_namespace(transdoc_rules)
handlers = transdoc.get_all_handlers()

repo = git.Repo(".")


transdoc.transform_tree(
    handlers,
    transformer,
    Path("input"),
    Path("output"),
    skip_if=lambda p: repo.ignored(path.absolute()),
)
```
