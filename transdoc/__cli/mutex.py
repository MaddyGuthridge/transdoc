"""# Transdoc / CLI / Mutex

Mutually exclusive option for Click argument parser.
"""

import click


class MutexError(click.UsageError):
    """Mutually-incompatible command-line options specified"""

    def __init__(
        self,
        self_name: str | None,
        mutex_opt: str,
        ctx: click.Context | None = None,
    ) -> None:
        super().__init__(
            f"Illegal usage: option '{self_name}' is mutually "
            f"exclusive with option '{mutex_opt}'.",
            ctx,
        )


class Mutex(click.Option):
    """Click option variant that is not required if another parameter is given.

    Adapted from https://stackoverflow.com/a/51235564/6335363 (CC BY-SA 4.0)
    """

    def __init__(self, *args, **kwargs) -> None:
        self.mutex_with: list = kwargs.pop("mutex_with")

        assert self.mutex_with, "'mutex_with' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "")
            + " Option is mutually exclusive with "
            + ", ".join(self.mutex_with)
            + "."
        ).strip()
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt = self.name in opts
        for mutex_opt in self.mutex_with:
            if mutex_opt in opts:
                if current_opt:
                    raise MutexError(self.name, mutex_opt, ctx)
                else:
                    self.required = False

        return super().handle_parse_result(ctx, opts, args)
