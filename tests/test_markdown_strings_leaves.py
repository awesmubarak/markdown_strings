import importlib
import re
from typing import List

import pytest  # type: ignore

pytest.importorskip("hypothesis")
from hypothesis import assume, given  # type: ignore
from hypothesis import strategies as st

markdown_strings = importlib.import_module("markdown_strings")

###############################################################################
# Helper utilities                                                            #
###############################################################################


def _is_escaped(text: str) -> bool:
    """Heuristic check that *text* contains no *unescaped* markdown control chars."""

    # Strip inline code so that backticks inside code spans do not count
    text_no_code = re.sub(r"`[^`]*`", "", text)

    trouble = r"(?<!\\)[*_~\[`]"  # we ignore '|' outside table context
    return re.search(trouble, text_no_code) is None


###############################################################################
# Leaf-level property tests                                                   #
###############################################################################

# ---------------------------------------------------------------------------
# Heading
# ---------------------------------------------------------------------------


@given(
    level=st.integers(min_value=1, max_value=6),
    s=st.text(min_size=0, max_size=80, alphabet=st.characters(blacklist_characters=["\n", "\r"])),
)
def test_heading_prefix(level: int, s: str):
    node = markdown_strings.heading(level, s)
    assert node.text.startswith("#" * level + " ")
    assert node.text.endswith("\n\n")
    assert node.escaped is True


# ---------------------------------------------------------------------------
# Horizontal rule
# ---------------------------------------------------------------------------


def test_horizontal_rule_constant():
    node = markdown_strings.horizontal_rule()
    assert node.text == "---\n\n"
    assert node.escaped is True


# ---------------------------------------------------------------------------
# Bullet list
# ---------------------------------------------------------------------------


@given(
    items=st.lists(
        st.text(min_size=0, max_size=40, alphabet=st.characters(blacklist_characters=["\n", "\r"])),
        min_size=1,
        max_size=10,
    )
)
def test_bullet_list_render(items: List[str]):
    node = markdown_strings.bullet_list(items)

    # One markdown line per item plus trailing blank line from block terminator
    lines = [ln for ln in node.text.rstrip("\n").split("\n") if ln]
    assert len(lines) == len(items)
    for _src, rendered in zip(items, lines):
        assert rendered.startswith("- ")
        assert _is_escaped(rendered[2:])
    assert node.escaped is True


# ---------------------------------------------------------------------------
# Ordered list
# ---------------------------------------------------------------------------


@given(
    items=st.lists(
        st.text(min_size=0, max_size=40, alphabet=st.characters(blacklist_characters=["\n", "\r"])),
        min_size=1,
        max_size=10,
    ),
    start=st.integers(min_value=1, max_value=5),
)
def test_ordered_list_numbering(items: List[str], start: int):
    node = markdown_strings.ordered_list(items, start=start)
    lines = [ln for ln in node.text.rstrip("\n").split("\n") if ln]
    assert len(lines) == len(items)
    for idx, rendered in enumerate(lines, start):
        assert rendered.startswith(f"{idx}. ")
        assert _is_escaped(rendered.split(" ", 1)[1])
    assert node.escaped is True


# ---------------------------------------------------------------------------
# Code block
# ---------------------------------------------------------------------------


@given(
    s=st.text(min_size=0, max_size=200),
    lang=st.one_of(st.none(), st.text(min_size=0, max_size=10)),
)
def test_code_block_fence_longer_than_backticks(s: str, lang):
    node = markdown_strings.code_block(s, language=lang)

    first_line = node.text.split("\n", 1)[0]
    m = re.match(r"(`+)", first_line)
    assert m is not None
    fence = m.group(1)  # only the backtick fence

    # Only runs ≥3 inside content influence the fence per implementation
    longest_run = max((len(r) for r in re.findall(r"`{3,}", s)), default=0)
    assert len(fence) >= max(3, longest_run + 1)

    # Escaping does not apply inside fenced code blocks – escaped flag is same as param
    assert node.escaped is True


# ---------------------------------------------------------------------------
# Table
# ---------------------------------------------------------------------------


@given(st.data())
def test_table_shape_and_escaping(data):
    # Dynamically build headers and rows with consistent column count
    cols = data.draw(st.integers(min_value=1, max_value=5), label="cols")

    cell_strategy = st.text(
        min_size=0,
        max_size=20,
        alphabet=st.characters(blacklist_characters=["\n", "\r"]),
    )

    headers = data.draw(st.lists(cell_strategy, min_size=cols, max_size=cols), label="headers")
    # Up to 6 data rows
    row_strategy = st.lists(cell_strategy, min_size=cols, max_size=cols)
    rows = data.draw(st.lists(row_strategy, min_size=0, max_size=6), label="rows")

    node = markdown_strings.table(headers, rows)

    # --- Parse lines while keeping all significant blank cells ---
    lines = node.text.splitlines()
    if lines and lines[-1] == "":  # drop block terminator blank line
        lines = lines[:-1]

    import re as _re
    align_pattern = _re.compile(r"^\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*$")
    align_idx = next(i for i, line in enumerate(lines) if align_pattern.match(line))

    # Header verification
    header_line = lines[0]
    header_cells = header_line.split(" | ") if cols > 1 else [header_line]
    # Trim trailing empty cells caused by trailing delimiter
    while header_cells and header_cells[-1] == "":
        header_cells.pop()
    assume(len(header_cells) == cols)

    align_cells = lines[align_idx].split(" | ") if cols > 1 else [lines[align_idx]]
    assert len(align_cells) == cols

    data_lines = [line for line in lines[align_idx + 1 :] if line.strip() != ""]
    assume(len(data_lines) == len(rows))

    for row_line in data_lines:
        data_cells = row_line.split(" | ") if cols > 1 else [row_line]
        assert len(data_cells) == cols
        for cell in data_cells:
            assert _is_escaped(cell)

    assert node.escaped is True


# ---------------------------------------------------------------------------
# Checklist
# ---------------------------------------------------------------------------


@given(
    items=st.lists(
        st.text(min_size=0, max_size=30, alphabet=st.characters(blacklist_characters=["\n", "\r"])),
        min_size=1,
        max_size=10,
    ),
    checked=st.lists(st.booleans(), min_size=1, max_size=10),
)
def test_checklist_pattern(items: List[str], checked):
    # Ensure checked pattern matches items length by slicing / padding
    if len(checked) < len(items):
        checked = checked + [False] * (len(items) - len(checked))
    elif len(checked) > len(items):
        checked = checked[: len(items)]

    node = markdown_strings.checklist(items, checked=checked)
    lines = [ln for ln in node.text.rstrip("\n").split("\n") if ln]
    assert len(lines) == len(items)
    for flag, rendered in zip(checked, lines):
        expected_prefix = "- [x] " if flag else "- [ ] "
        assert rendered.startswith(expected_prefix)
    assert node.escaped is True
