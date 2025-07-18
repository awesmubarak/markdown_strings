# Markdown Strings (ALPHA)

A type-safe Python package for generating Markdown.

This library provides a set of functions to build complex Markdown documents programmatically, with a focus on correctness and security. It ensures that all generated content is properly escaped, preventing common rendering issues and potential injection vulnerabilities.

## Table of Contents

- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Available Functions](#available-functions)
  - [Inline Elements](#inline-elements)
  - [Block Elements](#block-elements)
  - [Container Elements](#container-elements)
  - [Special Elements](#special-elements)
- [Composition](#composition)
- [Escaping and Safety](#escaping-and-safety)
- [Contributing](#contributing)
- [License](#license)

## Key Features

- **Type-Safe by Design**: The API is designed to prevent incorrect nesting of Markdown elements (e.g., block elements inside inline elements).
- **Secure by Default**: All string content is automatically escaped by default, preventing unintended Markdown interpretation and potential security vulnerabilities.
- **Safe Mode Protection**: An optional "safe mode" can be enabled to completely reject any unescaped content, ideal for applications handling untrusted input.
- **Comprehensive Markdown Support**: Supports a wide range of Markdown features, including headings, lists, tables, code blocks, and more.
- **Immutable Data Structures**: The core `MarkdownNode` is immutable, allowing for safe composition of Markdown fragments.

## Installation

```bash
pip install markdown_strings
```

*(Note: This package is not yet on PyPI. This is the intended installation command once published.)*

## Quick Start

You can generate inline Markdown fragments directly:

```python
import markdown_strings as md

print(md.bold("Make this bold"))
```

This will produce:

```markdown
**Make this bold**
```

Or you can build a whole Markdown document:

```python
import markdown_strings as md

doc = md.document([
    md.h1("My Markdown Document"),
    md.paragraph([
        "This is a paragraph containing ",
        md.bold("bold text"),
        " and ",
        md.italic("italic text"),
        "."
    ]),
    md.bullet_list([
        "First item",
        "Second item",
        "Third item",
    ]),
    md.code_block("print('Hello, World!')", language="python"),
])

print(doc)
```

This will produce the following Markdown output:

```markdown
# My Markdown Document

This is a paragraph containing **bold text** and *italic text*.

- First item
- Second item
- Third item

```python
print('Hello, World!')
```

Here's an example showing type-safe markdown generation from dynamic data:

```python
import markdown_strings as md

# Simulate API data (could be from any source)
pull_requests = [
    {"id": 101, "title": "Fix critical bug in <script>alert('xss')</script>", "author": "alice"},
    {"id": 102, "title": "Add **bold** formatting support", "author": "bob"},
    {"id": 103, "title": "Update README.md documentation", "author": "charlie"},
]

# Generate safe, structured markdown - all user content is automatically escaped
report = md.document([
    md.h1("🚀 Pull Request Report"),
    md.paragraph([
        "Generated on ", md.code("2025-06-28"), " for repository ", 
        md.bold("awesome-project/widget-factory"), "."
    ]),
    md.h2("Open Pull Requests"),
    md.bullet_list([
        [
            md.link(f"PR #{pr['id']}: {pr['title']}", f"https://github.com/repo/pull/{pr['id']}"),
            md.paragraph(f"Author: {md.italic(pr['author'])}")
        ]
        for pr in pull_requests
    ]),
    md.blockquote("All titles are automatically escaped for security! 🔒"),
])

print(report.text)
```

This produces safe, well-structured markdown where:
- **All user content is escaped** (notice the `<script>` tag becomes harmless text)
- **Complex nesting** works intuitively (links in lists, formatted text in paragraphs) 
- **Type safety** prevents invalid combinations at the API level

## Available Functions

This library provides a comprehensive set of functions for generating various Markdown elements.

### Inline Elements

These functions generate inline Markdown elements.

- `md.bold(content)`: Makes text bold.
- `md.italic(content)`: Makes text italic.
- `md.strikethrough(content)`: Creates strikethrough text.
- `md.code(content)`: Formats text as inline code.
- `md.link(text, url)`: Creates a hyperlink.
- `md.image(alt_text, url)`: Embeds an image.
- `md.reference_link(text, ref_id)`: Creates a link to a reference.
- `md.line_break()`: Adds a hard line break within a paragraph.

### Block Elements

These functions generate block-level Markdown elements.

- `md.paragraph(content)`: Creates a paragraph.
- `md.heading(level, content)`: Creates a heading of a specific level (1-6).
- `md.h1(content)`, `md.h2(content)`, ..., `md.h6(content)`: Shorthand for headings.
- `md.blockquote(content)`: Creates a blockquote.
- `md.code_block(content, language=None)`: Creates a block of code, with optional language highlighting.

### Container Elements

These functions create elements that can contain other elements.

- `md.document(children)`: Creates a full Markdown document.
- `md.bullet_list(items)`: Creates an unordered list.
- `md.ordered_list(items, start=1)`: Creates an ordered list.
- `md.checklist(items, checked=None)`: Creates a checklist.
- `md.table(headers, rows, alignment=None)`: Creates a table.

### Special Elements

These are special-purpose functions.

- `md.horizontal_rule()`: Creates a horizontal rule.
- `md.link_reference(ref_id, url)`: Defines a link reference.
- `md.empty()`: Represents an empty node, useful for conditional content.

## Composition

The functions in `markdown-strings` are designed to be composed together to build complex Markdown documents. You can nest inline elements within block elements, and block elements within container elements.

For example, you can create a list where some items are bold and others are italic:

```python
import markdown_strings as md

my_list = md.bullet_list([
    md.bold("This is a bold item"),
    md.italic("This is an italic item"),
    "This is a regular item"
])

print(my_list)
```

This produces:

```markdown
- **This is a bold item**
- *This is an italic item*
- This is a regular item
```

The exact rules for which elements can be nested inside others are still being finalised. As this is an alpha version, we encourage you to use your best judgment and experiment. The library will raise an `InvalidNestingError` if you attempt an invalid combination. Full documentation on composition rules will be available in a future release.

## Escaping and Safety

By default, `markdown_strings` automatically escapes all string content to ensure it renders as plain text, preventing unintended Markdown interpretation and potential security issues.

### Automatic Escaping

When you pass regular strings to any function, special Markdown characters are automatically escaped (taking into account the specific feature you're using):

```python
import markdown_strings as md

# These strings contain Markdown syntax, but will be escaped
text_with_markdown = "# This looks like a header\n* And this like a list"
result = md.paragraph(text_with_markdown)
print(result)
```

Output:
```markdown
\# This looks like a header
\* And this like a list
```

### Disabling Escaping

If you need to include raw Markdown content, you can disable escaping using the `escape=False` parameter available on most functions:

```python
import markdown_strings as md

# This will NOT be escaped - use with caution!
raw_markdown = "**This will be bold** and *this italic*"
result = md.paragraph(raw_markdown, escape=False)
print(result)
```

Output:
```markdown
**This will be bold** and *this italic*
```

**⚠️ Warning**: Only use `escape=False` with trusted content. Unescaped user input could potentially break your document structure.

### Safe Mode

For applications that handle untrusted input, you can enable "safe mode" to completely prevent unescaped content:

```python
import markdown_strings as md

# Enable safe mode globally
md.set_safe_mode(True)

# This will now raise an exception
try:
    result = md.paragraph("Some text", escape=False)
except md.SafeModeError as e:
    print(f"Safety violation: {e}")

# Check if safe mode is enabled
if md.is_safe_mode():
    print("Safe mode is active")

# Disable safe mode
md.set_safe_mode(False)
```

Safe mode is particularly useful in web applications, documentation generators, or any system that processes user-generated content.

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

### Development Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. To get started:

```bash
# Clone the repository
git clone https://github.com/awesmubarak/markdown_strings
cd markdown_strings

# Install dependencies
uv sync --group dev
```

### Code Quality

Before submitting a pull request, please ensure your code passes all quality checks by running these commands:

```bash
# Check code formatting and style
uv run ruff check .

# Type checking
uv run mypy src/

# Run tests
uv run pytest
```

All three commands should pass without errors before submitting your contribution.

## License

This project is licensed under the MIT License.
