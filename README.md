# Markdown Strings (ALPHA)

A Python package for generating GitHub-Flavoured Markdown in a type-safe way.

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
- [Contributing](#contributing)
- [License](#license)

## Key Features

- **Type-Safe by Design**: The API is designed to prevent incorrect nesting of Markdown elements (e.g., block elements inside inline elements).
- **Automatic Escaping**: All string content is automatically escaped by default to ensure it renders as plain text.
- **Safe Mode**: An optional "safe mode" can be enabled to reject any unescaped content, providing an extra layer of security.
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

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.