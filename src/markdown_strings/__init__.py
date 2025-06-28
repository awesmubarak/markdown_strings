"""A Python package for generating GitHub-Flavoured Markdown content."""

# Package metadata
__version__ = "4.0.0"
__author__ = "Awes Mubarak"
__email__ = "contact@awesmubarak.com"

from .core import (
    # Global helpers
    set_safe_mode,
    is_safe_mode,
    # Core data structures
    MarkdownNode,
    MarkdownString,
    # Exceptions
    MarkdownError,
    InvalidNestingError,
    ValidationError,
    SafeModeError,
    # Inline nodes
    bold,
    italic,
    code,
    strikethrough,
    link,
    image,
    # Block nodes
    paragraph,
    heading,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    blockquote,
    code_block,
    # Container nodes
    document,
    bullet_list,
    ordered_list,
    checklist,
    table,
    # Special nodes
    horizontal_rule,
    line_break,
    reference_link,
    link_reference,
    empty,
)

__all__ = [
    # Global helpers
    "set_safe_mode",
    "is_safe_mode",
    # Core data structures
    "MarkdownNode",
    "MarkdownString",
    # Exceptions
    "MarkdownError",
    "InvalidNestingError",
    "ValidationError",
    "SafeModeError",
    # Inline nodes
    "bold",
    "italic",
    "code",
    "strikethrough",
    "link",
    "image",
    # Block nodes
    "paragraph",
    "heading",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "blockquote",
    "code_block",
    # Container nodes
    "document",
    "bullet_list",
    "ordered_list",
    "checklist",
    "table",
    # Special nodes
    "horizontal_rule",
    "line_break",
    "reference_link",
    "link_reference",
    "empty",
] 