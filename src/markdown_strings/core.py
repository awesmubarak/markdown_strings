
"""Core module for a type-safe GitHub-Flavoured Markdown (GFM) generator.

This module implements the full public API described in the design
specification.  Every helper is intentionally kept private (prefixed with an
underscore) unless it forms part of the documented API surface.
"""

import re
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Union

__all__ = [
    # Global helpers
    "set_safe_mode",
    "is_safe_mode",
    # Core data structure
    "MarkdownNode",
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

###############################################################################
# Public data structure and exceptions                                       #
###############################################################################


@dataclass(frozen=True)
class MarkdownNode:
    """Immutable representation of a markdown fragment.

    Attributes
    ----------
    type:
        Symbolic identifier for the node (e.g. ``"bold"`` or ``"table"``).
    text:
        Rendered markdown text for this node **and** all children.
    escaped:
        ``True`` if **every** character inside *text* is properly escaped. A
        value of ``False`` signals that unescaped content may be present
        in the subtree so callers can implement additional safety checks.
    """

    type: str
    text: str
    escaped: bool

    # Human-friendly representation – great when debugging in the REPL.
    def __repr__(self) -> str:  # pragma: no cover – cosmetic only
        return (
            f"MarkdownNode(type={self.type!r}, escaped={self.escaped}, "
            f"text={self.text!r})"
        )


###############################################################################
# Global safe-mode toggle                                                    #
###############################################################################

# NOTE: We purposely keep the flag _private_ and only expose the getter /
# setter.  This discourages direct mutation by users.
_safe_mode_enabled: bool = False


def set_safe_mode(enabled: bool) -> None:
    """Enable or disable *safe mode*.

    When safe mode is active the library **rejects** any call where
    ``escape=False`` would result in injecting unescaped markdown directly into
    the output.  Attempting to do so raises :class:`SafeModeError`.
    """

    global _safe_mode_enabled
    _safe_mode_enabled = bool(enabled)


def is_safe_mode() -> bool:  # noqa: D401 – not a statement
    """Return ``True`` if *safe mode* is currently active."""

    return _safe_mode_enabled


###############################################################################
# Custom exception hierarchy                                                 #
###############################################################################


class MarkdownError(Exception):
    """Base class for all library-defined exceptions."""


class InvalidNestingError(MarkdownError):
    """Raised when a node receives a child type it is not allowed to contain."""


class ValidationError(MarkdownError):
    """Raised when a function argument fails validation."""


class SafeModeError(MarkdownError):
    """Raised when *safe mode* forbids an ``escape=False`` operation."""


###############################################################################
# Internal utility helpers                                                   #
###############################################################################


# Mapping of node name -> *allowed child node names*
_ALLOWED_CHILDREN: dict[str, set[str]] = {}

# ---------------------------------------------------------------------------
# Inline – single line span elements
# ---------------------------------------------------------------------------
_INLINE_NODES = {
    "bold",
    "italic",
    "code",
    "strikethrough",
    "link",
    "image",  # image itself counts as inline when embedded in a paragraph
    "reference_link",
    "line_break",
    "text",
}

# Populate _ALLOWED_CHILDREN for inline nodes (will be updated for each)

# Allowed sets will be filled further below after we define them fully


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _normalize_content(content: Union[str, "MarkdownNode", Sequence[Union[str, "MarkdownNode"]], None]) -> List[Union[str, "MarkdownNode"]]:
    """Return *content* as a flat **list** of strings / nodes."""

    if content is None:
        return [""]

    if isinstance(content, (str, MarkdownNode)):
        return [content]

    # Iterables (but **not** strings) – create list copy so we can iterate
    if isinstance(content, Iterable):  # type: ignore[arg-type]
        return list(content)  # shallow copy OK (elements are immutable)

    raise TypeError(f"Invalid content type: {type(content).__name__}")


# Every function uses the same regex to split input into *lines* so we can
# implement context-sensitive escaping rules (e.g. escaping leading ‘#’ or '-')
_LINE_SPLIT_RE = re.compile("\r?\n")


def _escape_common(text: str) -> str:
    """Escape characters common to **all** markdown contexts."""

    # We have to escape *backslash* first to avoid double-escaping later.
    replacements = {
        "\\": "\\\\",
        "*": r"\*",
        "_": r"\_",
        "`": r"\`",
        "~": r"\~",
        "[": r"\[",
        "]": r"\]",
        "(": r"\(",
        ")": r"\)",
        "<": r"\<",
        ">": r"\>",
        "&": r"\&",
    }
    for char, repl in replacements.items():
        text = text.replace(char, repl)
    return text


def _escape_leading_patterns(line: str) -> str:
    """Escape leading characters in *line* that have special meaning."""

    # Escape *#* when it's at the very beginning (heading).
    if line.startswith("#"):
        line = "\\" + line

    # Escape * -* or *+* when at beginning followed by whitespace.
    if line.startswith("- "):
        line = "\\-" + line[1:]
    elif line.startswith("+ "):
        line = "\\+" + line[1:]

    # Escape *ordered-list* pattern:  «number. »
    match = re.match(r"(\d+)\.\s", line)
    if match:
        span = match.group(0)
        line = line.replace(span, span.replace(".", "\\."), 1)

    return line


def escape_text(text: str, *, context: str | None = None) -> str:
    """Escape *text* according to the specified *context*.

    Parameters
    ----------
    text:
        Raw input text that should be rendered literally.
    context:
        Optional qualifier indicating where *text* will appear so that we can
        apply *additional* escaping rules (e.g. `"table_cell"` needs to escape
        `|`).  When *None* only the common rules apply.
    """

    text = _escape_common(text)

    # Apply context-specific escaping rules.
    if context == "table_cell":
        text = text.replace("|", r"\|")
    elif context == "url":
        # Minimal URL escaping: encode spaces + parentheses.
        text = (
            text.replace(" ", "%20")
            .replace("(", "%28")
            .replace(")", "%29")
        )
    # No else -> no additional rules

    # Finally handle *line-specific* leading escapes.  We do this *after* the
    # context escapes but *before* returning because replacements above may
    # have introduced new line breaks.
    escaped_lines = [_escape_leading_patterns(line) for line in _LINE_SPLIT_RE.split(text)]
    return "\n".join(escaped_lines)


###############################################################################
# Allow-list population                                                      #
###############################################################################

# The design spec expresses allowed nesting as *sets* of node type names.
# Because we reference these sets both from multiple helpers *and* from the
# public node constructors we define them **once** centrally.

BOLD_ACCEPTS = {
    "text",
    "italic",
    "code",
    "strikethrough",
    "link",
    "bold",  # nested bold technically allowed, yields ****content****
}
ITALIC_ACCEPTS = {
    "text",
    "bold",
    "code",
    "strikethrough",
    "link",
    "italic",
}
CODE_ACCEPTS: set[str] = set()  # strings only
STRIKE_ACCEPTS = {
    "text",
    "bold",
    "italic",
    "code",
    "link",
    # Note: strikethrough cannot contain strikethrough
}
LINK_TEXT_ACCEPTS = {
    "text",
    "bold",
    "italic",
    "code",
    "strikethrough",
}
HEADING_ACCEPTS = LINK_TEXT_ACCEPTS
PARAGRAPH_ACCEPTS = LINK_TEXT_ACCEPTS | {"image", "line_break"}

# Update global mapping (inline nodes first)
_ALLOWED_CHILDREN.update(
    {
        "bold": BOLD_ACCEPTS,
        "italic": ITALIC_ACCEPTS,
        "code": CODE_ACCEPTS,
        "strikethrough": STRIKE_ACCEPTS,
        "link": LINK_TEXT_ACCEPTS,
        "reference_link": LINK_TEXT_ACCEPTS,
        "image": set(),  # strings only inside alt text → handled separately
        "line_break": set(),
    }
)

# Block / container nodes – we add later after function definitions to avoid
# forward-reference issues.

###############################################################################
# Core builder helpers                                                       #
###############################################################################


def _build_inline(
    type_name: str,
    delimiter_left: str,
    delimiter_right: str,
    content: Union[str, MarkdownNode, Sequence[Union[str, MarkdownNode]], None],
    *,
    accepts: set[str],
    escape: bool = True,
    process_item=lambda x: x,  # Identity by default. Override for special cases
) -> MarkdownNode:
    """Shared logic for inline nodes such as *bold* and *italic*."""

    if not escape and is_safe_mode():
        raise SafeModeError("escape=False is disabled in safe mode")

    items = _normalize_content(content)

    escaped_flag = escape
    parts: list[str] = []

    for item in items:
        if isinstance(item, str):
            parts.append(escape_text(item, context=type_name) if escape else item)
            continue

        if not isinstance(item, MarkdownNode):
            raise TypeError(f"Invalid content type: {type(item).__name__}")

        if item.type not in accepts:
            raise InvalidNestingError(f"{type_name} cannot contain node '{item.type}'")

        parts.append(item.text)
        if not item.escaped:
            escaped_flag = False

    # Apply post-processing *after* we assembled each part (useful for code).
    body = "".join(parts)
    body = process_item(body)
    rendered = f"{delimiter_left}{body}{delimiter_right}"

    return MarkdownNode(type=type_name, text=rendered, escaped=escaped_flag)


###############################################################################
# Inline node constructors                                                   #
###############################################################################


def bold(content: Union[str, MarkdownNode, Sequence[Union[str, MarkdownNode]], None], *, escape: bool = True) -> MarkdownNode:
    """Return **bold** markdown for *content*."""

    return _build_inline("bold", "**", "**", content, accepts=BOLD_ACCEPTS, escape=escape)


def italic(content: Union[str, MarkdownNode, Sequence[Union[str, MarkdownNode]], None], *, escape: bool = True) -> MarkdownNode:
    """Return *italic* markdown for *content*."""

    return _build_inline("italic", "*", "*", content, accepts=ITALIC_ACCEPTS, escape=escape)


# ---------------------------------------------------------------------------
# Inline code – requires custom fence calculation
# ---------------------------------------------------------------------------


def _code_fence_for(text: str) -> str:
    """Return backtick sequence ≥ longest run in *text* + 1 backtick."""

    longest = max((len(m.group(0)) for m in re.finditer(r"`+", text)), default=0)
    return "`" * (longest + 1 or 1)


def code(content: str, *, escape: bool = True) -> MarkdownNode:  # type: ignore[override]
    """Return inline ``code`` markdown.

    *content* **must** be a string per spec; embedding nodes inside inline code
    is intentionally disallowed to avoid partially escaped segments.
    """

    if not isinstance(content, str):
        raise TypeError("code() only accepts raw strings")

    if not escape and is_safe_mode():
        raise SafeModeError("escape=False is disabled in safe mode")

    fence = _code_fence_for(content)
    body = content if not escape else escape_text(content, context="code")

    rendered = f"{fence}{body}{fence}"
    return MarkdownNode(type="code", text=rendered, escaped=escape)


# ---------------------------------------------------------------------------
# Strikethrough
# ---------------------------------------------------------------------------

def strikethrough(content: Union[str, MarkdownNode, Sequence[Union[str, MarkdownNode]], None], *, escape: bool = True) -> MarkdownNode:
    """Return ~~strikethrough~~ markdown."""

    return _build_inline(
        "strikethrough",
        "~~",
        "~~",
        content,
        accepts=STRIKE_ACCEPTS,
        escape=escape,
    )


# ---------------------------------------------------------------------------
# Links and images require extra processing
# ---------------------------------------------------------------------------


def link(
    text: Union[str, MarkdownNode, Sequence[Union[str, MarkdownNode]], None],
    url: str,
    *,
    escape: bool = True,
) -> MarkdownNode:
    """Return a markdown hyperlink ``[text](url)``.

    The *url* **always** behaves as if ``escape=True`` (spaces are converted to
    *%20*, parentheses are escaped) irrespective of the *escape* argument which
    only affects the *link text*.
    """

    if not isinstance(url, str):
        raise TypeError("url must be string")

    escaped_url = escape_text(url, context="url")

    node = _build_inline(
        "link",
        "[",
        f"]({escaped_url})",
        text,
        accepts=LINK_TEXT_ACCEPTS,
        escape=escape,
    )
    return node


def image(alt_text: str, url: str, *, escape: bool = True) -> MarkdownNode:
    """Return an image ``![alt_text](url)`` markdown node."""

    if not isinstance(alt_text, str) or not isinstance(url, str):
        raise TypeError("alt_text and url must be strings")

    if not escape and is_safe_mode():
        raise SafeModeError("escape=False is disabled in safe mode")

    alt = escape_text(alt_text, context="image") if escape else alt_text
    escaped_url = escape_text(url, context="url")

    rendered = f"![{alt}]({escaped_url})"
    return MarkdownNode(type="image", text=rendered, escaped=escape)


# ---------------------------------------------------------------------------
# Line break & empty helpers
# ---------------------------------------------------------------------------


def line_break() -> MarkdownNode:
    """Return a hard line-break (two spaces + newline)."""

    return MarkdownNode(type="line_break", text="  \n", escaped=True)


def empty() -> MarkdownNode:
    """Return an always-escaped empty string node."""

    return MarkdownNode(type="empty", text="", escaped=True)


###############################################################################
# Block node constructors                                                    #
###############################################################################


# ---------------------------------------------------------------------------
# Paragraph & heading share common helper
# ---------------------------------------------------------------------------


_BLOCK_TERMINATOR = "\n\n"  # All block nodes end with blank line (GFM spec)


def _join_inline_items(items: Sequence[str]) -> str:
    """Concatenate *items* without introducing *unexpected* whitespace."""

    return "".join(items)



def paragraph(content: Union[str, MarkdownNode, Sequence[Union[str, MarkdownNode]], None], *, escape: bool = True) -> MarkdownNode:
    """Return a markdown paragraph which terminates with a blank line."""

    node = _build_inline(
        "paragraph",
        "",
        _BLOCK_TERMINATOR,
        content,
        accepts=PARAGRAPH_ACCEPTS,
        escape=escape,
    )
    return node


# ---------------------------------------------------------------------------
# Headings (h1-h6)
# ---------------------------------------------------------------------------

def heading(level: int, content: Union[str, MarkdownNode, Sequence[Union[str, MarkdownNode]], None], *, escape: bool = True) -> MarkdownNode:
    """Return ATX-style heading at *level* (1–6)."""

    if level not in range(1, 7):
        raise ValidationError(f"heading level must be between 1 and 6, got {level}")

    prefix = "#" * level + " "
    node = _build_inline(
        "heading",
        prefix,
        _BLOCK_TERMINATOR,
        content,
        accepts=HEADING_ACCEPTS,
        escape=escape,
    )
    return node


# Convenience wrappers.

def h1(content, *, escape: bool = True):  # noqa: D401 – no return type for brevity
    return heading(1, content, escape=escape)

def h2(content, *, escape: bool = True):
    return heading(2, content, escape=escape)

def h3(content, *, escape: bool = True):
    return heading(3, content, escape=escape)

def h4(content, *, escape: bool = True):
    return heading(4, content, escape=escape)

def h5(content, *, escape: bool = True):
    return heading(5, content, escape=escape)

def h6(content, *, escape: bool = True):
    return heading(6, content, escape=escape)


# ---------------------------------------------------------------------------
# Block quote
# ---------------------------------------------------------------------------


def blockquote(content: Union[str, MarkdownNode, Sequence[Union[str, MarkdownNode]], None], *, escape: bool = True) -> MarkdownNode:
    """Return a markdown block quote (> …)."""

    if not escape and is_safe_mode():
        raise SafeModeError("escape=False is disabled in safe mode")

    # We take a simpler route: generate paragraph-style body first then prefix
    # each *line* with '> '.  We have to be careful to preserve blank line at
    # the end.
    body_node = paragraph(content, escape=escape)
    lines = body_node.text.rstrip().split("\n")
    prefixed = "\n".join("> " + line if line.strip() else ">" for line in lines)
    rendered = prefixed + _BLOCK_TERMINATOR

    escaped_flag = body_node.escaped and escape
    return MarkdownNode(type="blockquote", text=rendered, escaped=escaped_flag)


# ---------------------------------------------------------------------------
# Code block
# ---------------------------------------------------------------------------


def _code_block_fence_for(text: str) -> str:
    longest = max((len(m.group(0)) for m in re.finditer(r"`{3,}", text)), default=0)
    return "`" * max(3, longest + 1)


def code_block(content: str, *, language: str | None = None, escape: bool = True) -> MarkdownNode:
    """Return fenced code block (```lang\n…\n```)."""

    if not isinstance(content, str):
        raise TypeError("code_block() only accepts raw strings for content")

    if not escape and is_safe_mode():
        raise SafeModeError("escape=False is disabled in safe mode")

    fence = _code_block_fence_for(content)
    lang_part = language or ""

    body = content if not escape else escape_text(content, context="code_block")
    rendered = f"{fence}{lang_part}\n{body}\n{fence}{_BLOCK_TERMINATOR}"
    return MarkdownNode(type="code_block", text=rendered, escaped=escape)


###############################################################################
# Container nodes                                                            #
###############################################################################


# ---------------------------------------------------------------------------
# Document root
# ---------------------------------------------------------------------------

# We'll fill ALLOWED_CHILDREN for container nodes now that all block functions
# exist.
_ALLOWED_CHILDREN.update(
    {
        "paragraph": set(PARAGRAPH_ACCEPTS),
        "heading": set(HEADING_ACCEPTS),
        "blockquote": set(PARAGRAPH_ACCEPTS),  # simplification
        "code_block": set(),
    }
)


def document(children: Sequence[MarkdownNode]) -> MarkdownNode:
    """Return a complete markdown *document* (no extra newline at EOF)."""

    if not isinstance(children, Sequence):
        raise TypeError("document() expects a sequence of MarkdownNode children")

    parts: list[str] = []
    escaped_flag = True

    for child in children:
        if not isinstance(child, MarkdownNode):
            raise TypeError("All children of document() must be MarkdownNode")
        parts.append(child.text.rstrip("\n"))
        if not child.escaped:
            escaped_flag = False
    rendered = "\n".join(parts)
    return MarkdownNode(type="document", text=rendered, escaped=escaped_flag)


# ---------------------------------------------------------------------------
# Lists (bullet, ordered, checklist)
# ---------------------------------------------------------------------------


def _render_list_items(
    items: Sequence[Union[str, MarkdownNode, Sequence]],
    *,
    level: int = 0,
    ordered: bool = False,
    start: int = 1,
    checklist: bool = False,
    checked_pattern: Sequence[bool] | None = None,
    escape: bool = True,
) -> tuple[str, bool]:
    """Recursive helper that renders nested lists and returns (text, escaped)."""

    parts: list[str] = []
    idx = start
    escaped_flag = escape

    for i, item in enumerate(items):
        prefix: str
        if ordered and not checklist:
            prefix = f"{idx}. "
            idx += 1
        elif checklist:
            checked = bool(checked_pattern[i]) if checked_pattern else False
            prefix = "- [x] " if checked else "- [ ] "
        else:
            prefix = "- "

        indent = "  " * level

        if isinstance(item, Sequence) and not isinstance(item, (str, MarkdownNode)):
            # Nested list – render recursively
            nested_text, nested_escaped = _render_list_items(
                item,
                level=level + 1,
                ordered=ordered,
                start=1,
                checklist=checklist,
                checked_pattern=None,
                escape=escape,
            )
            item_text = nested_text
            if not nested_escaped:
                escaped_flag = False
            rendered = f"{indent}{prefix}\n{item_text}"
            parts.append(rendered)
            continue

        # Regular item
        if isinstance(item, str):
            text = escape_text(item, context="list") if escape else item
            parts.append(f"{indent}{prefix}{text}")
        elif isinstance(item, MarkdownNode):
            parts.append(f"{indent}{prefix}{item.text.strip()}")
            if not item.escaped:
                escaped_flag = False
        else:
            raise TypeError(f"Invalid list item type: {type(item).__name__}")

    rendered = "\n".join(parts) + _BLOCK_TERMINATOR
    return rendered, escaped_flag


def bullet_list(items: Sequence[Union[str, MarkdownNode, Sequence]], *, escape: bool = True) -> MarkdownNode:
    """Return unordered list markdown."""

    text, escaped_flag = _render_list_items(items, escape=escape)
    return MarkdownNode(type="bullet_list", text=text, escaped=escaped_flag)


def ordered_list(
    items: Sequence[Union[str, MarkdownNode, Sequence]],
    *,
    start: int = 1,
    escape: bool = True,
) -> MarkdownNode:
    """Return ordered list markdown starting at *start*."""

    if start < 1:
        raise ValidationError("ordered_list start must be positive integer")

    text, escaped_flag = _render_list_items(items, ordered=True, start=start, escape=escape)
    return MarkdownNode(type="ordered_list", text=text, escaped=escaped_flag)


def checklist(
    items: Sequence[Union[str, MarkdownNode]],
    *,
    checked: Sequence[bool] | None = None,
    escape: bool = True,
) -> MarkdownNode:
    """Return GFM task list (checklist)."""

    if checked is not None and len(checked) != len(items):
        raise ValidationError("checked list length must match items length")

    text, escaped_flag = _render_list_items(items, checklist=True, checked_pattern=checked or [], escape=escape)
    return MarkdownNode(type="checklist", text=text, escaped=escaped_flag)


# ---------------------------------------------------------------------------
# Horizontal rule
# ---------------------------------------------------------------------------


def horizontal_rule() -> MarkdownNode:
    """Return `---` horizontal rule."""

    return MarkdownNode(type="horizontal_rule", text="---\n\n", escaped=True)


# ---------------------------------------------------------------------------
# Table
# ---------------------------------------------------------------------------


def validate_alignment(alignment: Sequence[str] | None, columns: int) -> None:
    if alignment is None:
        return
    if len(alignment) != columns:
        raise ValidationError("alignment list must match number of columns")
    valid = {"left", "center", "right"}
    for a in alignment:
        if a not in valid:
            raise ValidationError(f"Invalid alignment value '{a}' – must be left|center|right")


def _render_table_cell(item: Union[str, MarkdownNode], *, escape: bool) -> tuple[str, bool]:
    if isinstance(item, str):
        text = escape_text(item, context="table_cell") if escape else item
        return text, escape
    if isinstance(item, MarkdownNode):
        return item.text, item.escaped
    raise TypeError("Table cells must be string or MarkdownNode")


def table(
    headers: Sequence[Union[str, MarkdownNode]],
    rows: Sequence[Sequence[Union[str, MarkdownNode]]],
    *,
    alignment: Sequence[str] | None = None,
    escape: bool = True,
) -> MarkdownNode:
    """Return a markdown table node."""

    num_cols = len(headers)
    if num_cols == 0:
        raise ValidationError("table must have at least 1 header column")

    validate_alignment(alignment, num_cols)

    for r, row in enumerate(rows, 1):
        if len(row) != num_cols:
            raise ValidationError(
                f"table row {r} has {len(row)} columns but headers have {num_cols}"
            )

    # Render header row
    header_cells: list[str] = []
    escaped_flag = escape
    for cell in headers:
        text, cell_escaped = _render_table_cell(cell, escape=escape)
        header_cells.append(text)
        if not cell_escaped:
            escaped_flag = False

    header_line = " | ".join(header_cells)

    # Alignment row
    if alignment is None:
        align_row = " | ".join(["---"] * num_cols)
    else:
        align_map = {
            "left": ":---",
            "center": ":---:",
            "right": "---:",
        }
        align_row = " | ".join(align_map[a] for a in alignment)

    # Render data rows
    row_lines: list[str] = []
    for row in rows:
        row_cells: list[str] = []
        for cell in row:
            text, cell_escaped = _render_table_cell(cell, escape=escape)
            row_cells.append(text)
            if not cell_escaped:
                escaped_flag = False
        row_lines.append(" | ".join(row_cells))

    rendered = " | ".join(header_cells)
    lines = [header_line, align_row, *row_lines]
    rendered = "\n".join(lines) + _BLOCK_TERMINATOR

    return MarkdownNode(type="table", text=rendered, escaped=escaped_flag)


###############################################################################
# Link references (reference style)                                          #
###############################################################################


def reference_link(text: Union[str, MarkdownNode, Sequence[Union[str, MarkdownNode]], None], ref_id: str, *, escape: bool = True) -> MarkdownNode:
    """Return a reference link ``[text][ref_id]`` (definition created separately)."""

    if not isinstance(ref_id, str):
        raise TypeError("ref_id must be string")

    id_escaped = escape_text(ref_id, context="url")  # treat as url fragment

    node = _build_inline(
        "reference_link",
        "[",
        f"][{id_escaped}]",
        text,
        accepts=LINK_TEXT_ACCEPTS,
        escape=escape,
    )
    return node


def link_reference(ref_id: str, url: str) -> MarkdownNode:
    """Return the definition part of reference link ``[id]: url``."""

    if not isinstance(ref_id, str) or not isinstance(url, str):
        raise TypeError("ref_id and url must be strings")

    rendered = f"[{ref_id}]: {escape_text(url, context='url')}\n"
    return MarkdownNode(type="link_reference", text=rendered, escaped=True)


###############################################################################
# House-keeping: hide helper names from * import                             #
###############################################################################