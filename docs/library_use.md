# Using Transdoc programmatically

Transdoc can be used to transform files and text programmatically.

## Creating a rule-set

Transdoc represents rule-sets using `TransdocTransformer` objects.

::: transdoc.TransdocTransformer

## Collecting handlers

[Handlers](./handlers.md) are used to handle various file-types to ensure
information is transformed correctly (eg by preventing nested sets from being
transformed in Python source code).

You can load all available handlers using `transdoc.handlers.get_all_handlers`.
You can also implement the
[`transdoc.handlers.TransdocHandler`][transdoc.handlers.TransdocHandler]
protocol to create your own handlers.

::: transdoc.get_all_handlers

## Transforming inputs

You can transform text by using the following functions.

::: transdoc.transform

::: transdoc.transform_file

::: transdoc.transform_tree
