"""
# Transdoc / Collect rules

Code for collecting rules from a module.
"""

import sys
import importlib.util
from pathlib import Path
from .__rule import TransdocRule


def load_rule_file(rule_file: Path) -> dict[str, TransdocRule]:
    """
    Load a Python rule file given its path, returning a mapping of its rules.

    Items are considered to be rules if they are callable, and if there is an
    `__all__` attribute in the module, if they are contained within it.
    """
    # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    module_name = f"transdoc.rules_temp.{rule_file.name.removesuffix('.py')}"

    spec = importlib.util.spec_from_file_location(module_name, rule_file)
    if spec is None:
        raise ImportError(f"Import spec for rule file '{rule_file}' was None")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    if spec.loader is None:
        raise ImportError(f"Spec loader for rule file '{rule_file}' was None")

    # Any exceptions this raises get caught by the calling code
    try:
        spec.loader.exec_module(module)
    except BaseException as e:
        e.add_note(
            f"This exception occurred during execution of rule file "
            f"{rule_file}. It is unlikely to be an issue with Transdoc."
        )
        raise e

    items = getattr(module, "__all__", dir(module))

    collected_rules = {}

    for item_name in items:
        item = getattr(module, item_name)
        if callable(item):
            collected_rules[item_name] = item

    return collected_rules
