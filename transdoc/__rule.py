"""# Transdoc / rule

Type definition for Transdoc rules
"""
from collections.abc import Callable

TransdocRule = Callable[..., str]
"""
Rules are Python functions (potentially accepting arguments) which can be
called within Transdoc input files.
"""
