# Markdown_strings package

Markdown is a markup language with plain text formatting syntax. This package
allows the creation of markdown-compliant strings. The following is a summary
of features with usage examples.

Note: asterisk and underscores are escaped for all functions that do not format
to code (`inline_code` and `code_block`).

## Standard markdown features

### Header

Return a header of specified level.

Keyword arguments:

-   style -- Specifies the header style (default atx). The "atx" style uses
    hash signs, and has 6 levels. The "setext" style uses dashes or equals
    signs for headers of levels 1 and 2 respectively, and is limited to
    those two levels. The number of dashes or equals signs is either the length
    of the text, or 3.

Specifying a level outside of the style's range results in a ValueError.

```python
>>> header("Main Title", 1)
'# Main Title'
>>> header("Smaller subtitle", 4)
'#### Smaller subtitle'
>>> header("Setext style", 2, "setext")
'Setext style\n---'
```

### Italics

Return italics formatted text.

```Python
>>> italics("This text is italics")
'_This text is italics_'
```

### Bold

Return bold formatted text.

```python
>>> bold("This text is bold")
'**This text is bold**'
```

### Inline code

Return formatted inline code.

```python
>>> inline_code("This text is code")
'`This text is code`'
```

### Code block

Return a code block.

If a language is specified a fenced code block is produced, otherwise the
block is indented by four spaces.

Keyword arguments:

-   language -- Specifies the language to fence the code in (default blank).

````python
    >>> code_block("This is a simple codeblock.")
    '    This is a simple codeblock.'
    >>> code_block("This is a simple codeblock.\\nBut it has a linebreak!")
    '    This is a simple codeblock.\\n    But it has a linebreak!'
    >>> code_block("This block of code has a specified language.", "python")
    '```python\\nThis block of code has a specified language.\\n```'
    >>> code_block("So\\nmany\\nlinebreaks.", "python")
    '```python\\nSo\\nmany\\nlinebreaks.\\n```'
````

### Link

Return an inline link.

```python
>>> link ("This is a link", "https://github.com/awesmubarak/markdown_strings")
'[This is a link](https://github.com/awesmubarak/markdown_strings)'
```

### Image

Return an inline image.

Keyword arguments:

-   title -- Specify the title of the image, as seen when hovering over it.

```python
>>> image("This is an image", "https://avatars3.githubusercontent.com/u/24862378")
'![This is an image](https://avatars3.githubusercontent.com/u/24862378)'
>>> image("This is an image", "https://avatars3.githubusercontent.com/u/24862378", "awes")
'![This is an image](https://avatars3.githubusercontent.com/u/24862378) "awes"'
```

### Unordered list

Return an unordered list from an list.

```python
>>> unordered_list(["first", "second", "third", "fourth"])
'-   first\\n-   second\\n-   third\\n-   fourth'
>>> unordered_list([1, 2, 3, 4, 5])
'-   1\\n-   2\\n-   3\\n-   4\\n-   5'
```

### Ordered list

Return an ordered list from an list.

```python
>>> ordered_list(["first", "second", "third", "fourth"])
'1.  first\\n2.  second\\n3.  third\\n4.  fourth'
```

### Blockquote

Return a blockquote.

```python
>>> blockquote("A simple blockquote")
'> A simple blockquote'
```

### Horizontal rule

Return a horizontal rule.

Keyword arguments:

-   length -- Specifies the length of the rule (default 79, minimum 3).
-   style -- Character used for the rule (may be either "\_" or "\*").

If the length is too low, or the style is invalid, a ValueError is raised.

```python
>>> horizontal_rule()
'_______________________________________________________________________________'
>>> horizontal_rule(length=5, style="*")
'*****'
```

## Non-standard markdown

### Strikethrough

Return text with strike-through formatting.

```python
>>> strikethrough("This is a lie")
'~This is a lie~'
```

### Task list

Return a task list.

The task_list should be a 2-dimensional iterable; the first item should be the
task text and the second the boolean completion state.

```python
>>> task_list([["Be born", True], ["Be dead", False]])
'- [X] Be born\\n- [ ] Be dead'
```

### Table row

Return a single table row.

Keyword arguments:

-   pad -- The pad should be an list of the same size as the input text list.
    It will be used to format the row's padding.

```python
>>> table_row(["First column", "Second", "Third"])
'| First column | Second | Third |'
>>> table_row(["First column", "Second", "Third"], [10, 10, 10])
'| First column | Second     | Third      |'
```

### Delimiter row

Return a delimiter row for use in a table.

```python
>>> table_delimiter_row(3)
'| --- | --- | --- |'
```

### Table

Return a formatted table, generated from lists representing columns.

The function requires a 2-dimensional list, where each list is a column
of the table. This will be used to generate a formatted table in string
format.

```python
>>> table([["1","2","3"], ["4","5","6"], ["7","8","9"]])
'| 1 | 4 | 7 |\\n| --- | --- | --- |\\n| 2 | 5 | 8 |\\n| 3 | 6 | 9 |'

>>> table([["Name", "Awes", "Bob"], ["User", "mub123", ""]])
'| Name | User   |\\n| ---- | ------ |\\n| Awes | mub123 |\\n| Bob  |        |'
```

This table, when parsed, will look like this:

| Name | User   |
| ---- | ------ |
| Awes | mub123 |
| Bob  |        |

### Table from rows

Return a formatted table, using each list as the list. The specifics are the
same as those for the table function.

```python
>>> table_from_rows([["1","2","3"],["4","5","6"],["7","8","9"]])
'| 1 | 2 | 3 |\\n| --- | --- | --- |\\n| 4 | 5 | 6 |\\n| 7 | 8 | 9 |'
```

## Helper functions

Return text with formatting escaped

Markdown requires a backslash before literal underscores or asterisk, to avoid
formatting to bold or italics.

```python
>>> esc_format("Normal text")
'Normal text'
>>> esc_format("Text with **bold**")
'Text with \*\*bold\*\*'
>>> esc_format("Text with _italics_")
'Text with \_italics\_'
>>> esc_format("Text with _**complicated** formatting_")
'Text with \_\*\*complicated\*\* formatting\_'
```
