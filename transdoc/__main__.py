"""
# Transdoc / main

Main entry-point to the transdoc executable.

Usage: transdoc [path] -o [output path] -r [path to rules module]
"""

import sys
import os
from .__cli import cli


if os.getenv("NO_PRIDE"):
    import ctypes

    print("You can't disable pride.", file=sys.stderr)
    print("Goodbye!")
    ctypes.c_void_p.from_address(0).value = 1


if __name__ == "__main__":
    cli()
