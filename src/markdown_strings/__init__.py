"""markdown_strings public API.

This package exposes a clean public interface for generating Markdown
content.  All functionality lives in the :pymod:`markdown_strings.core`
module but is re-exported here for convenience.
"""

# Package metadata
__version__ = "4.0.0"
__author__ = "Awes Mubarak"
__email__ = "contact@awesmubarak.com"

# Re-export the full public surface from ``core`` so that users can simply
# ``import markdown_strings as md``.
from .core import *  # noqa: F401,F403 – re-export intentional
from . import core as _core

__all__ = _core.__all__ 