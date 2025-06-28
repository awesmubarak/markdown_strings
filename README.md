# Markdown Strings (ALPHA)

A Python package for generating GitHub-Flavoured Markdown in a type-safe way.

This library provides a set of functions to build complex Markdown documents programmatically, with a focus on correctness and security. It ensures that all generated content is properly escaped, preventing common rendering issues and potential injection vulnerabilities.

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

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.