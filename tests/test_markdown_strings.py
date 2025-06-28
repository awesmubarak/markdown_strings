import importlib
import re
from typing import List, Tuple

import pytest  # type: ignore

# Hypothesis for property-based testing (pytest integration)
pytest.importorskip("hypothesis")
from hypothesis import given  # type: ignore
from hypothesis import strategies as st

markdown_strings = importlib.import_module("markdown_strings")

###############################################################################
# Helper utilities                                                            #
###############################################################################


def _is_escaped(text: str) -> bool:
    """Heuristic check that *text* contains no *unescaped* markdown control chars."""

    # Strip inline code so that backticks inside code spans do not count
    text_no_code = re.sub(r"`[^`]*`", "", text)

    # Pattern of potentially dangerous chars when *not* preceded by a backslash
    trouble = r"(?<!\\)[*_~\[`]"
    return re.search(trouble, text_no_code) is None


###############################################################################
# Property-based tests                                                        #
###############################################################################


# ---------------------------------------------------------------------------
# Character-safety (leaf-level)
# ---------------------------------------------------------------------------


@given(st.text(min_size=0, max_size=100))
def test_bold_escapes_inner_text(s: str):
    """Escaping lemma: bold(x) is **y** where y is fully escaped."""

    result = markdown_strings.bold(s)
    inner = str(result)[2:-2]  # remove surrounding **
    assert _is_escaped(inner)
    assert result.escaped is True


@given(st.text(min_size=0, max_size=100))
def test_code_fence_longer_than_backticks_inside(s: str):
    """Fence construction invariant for inline code spans."""

    node = markdown_strings.code(s)
    m = re.match(r"(`+)", node.text)
    assert m is not None
    fence = m.group(1)
    longest_run = max((len(r) for r in re.findall(r"`+", s)), default=0)
    assert len(fence) >= longest_run + 1


# ---------------------------------------------------------------------------
# Escape propagation (taint-analysis lattice)
# ---------------------------------------------------------------------------


@given(st.lists(st.tuples(st.text(min_size=0, max_size=20), st.booleans()), min_size=1, max_size=8))
def test_escape_flag_is_conservative(items: List[Tuple[str, bool]]):
    """Parent.escaped == all(child.escaped) (join rule)."""

    children = [markdown_strings.bold(t, escape=esc) for t, esc in items]
    para = markdown_strings.paragraph(children)
    assert para.escaped == all(child.escaped for child in children)


# ---------------------------------------------------------------------------
# Monotone information-flow
# ---------------------------------------------------------------------------


@given(st.text(min_size=1, max_size=40))
def test_unsafe_child_propagates_upwards(s: str):
    unsafe_leaf = markdown_strings.bold(s, escape=False)
    doc = markdown_strings.document([markdown_strings.paragraph([unsafe_leaf])])
    assert doc.escaped is False


# ---------------------------------------------------------------------------
# Invalid constructions are rejected (type-safety)
# ---------------------------------------------------------------------------


@given(st.text(min_size=0, max_size=30))
def test_block_inside_inline_is_forbidden(s: str):
    block = markdown_strings.paragraph(s)
    with pytest.raises(markdown_strings.InvalidNestingError):
        markdown_strings.bold(block)


# ---------------------------------------------------------------------------
# Safe-mode forbids raw injection
# ---------------------------------------------------------------------------


@given(st.text(min_size=0, max_size=30))
def test_safe_mode_blocks_unescaped(s: str):
    markdown_strings.set_safe_mode(True)
    try:
        with pytest.raises(markdown_strings.SafeModeError):
            markdown_strings.bold(s, escape=False)
    finally:
        markdown_strings.set_safe_mode(False)
