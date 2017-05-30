========================
Markdown_strings package
========================

Markdown is a markup language with plain text formatting syntax. This package
allows the creation of markdown-compliant strings. The following is a summary
of features with usage examples.

Note: asterisk and underscores are escaped for all functions that do not format
to code (inline_code and code_block).

Standard markdown features
==========================

Header
------

Return a header of specified level.
::

    >>> header("Main Title", 1)
    '# Main Title'
    >>> header("Smaller subtitle", 4)
    '#### Smaller subtitle'


Italics
-------

Return italics formatted text.
::

    >>> italics("This text is italics")
    '_This text is italics_'


Bold
----

Return bold formatted text.
::

    >>> bold("This text is bold")
    '**This text is bold**'


Inline code
-----------

Return formatted inline code.
::

    >>> inline_code("This text is code")
    '`This text is code`'


Code block
----------

Return a code block.

If a language is specified a fenced code block is produced, otherwise the
block is indented by four spaces.

Keyword arguments:
    language -- Specifies the language to fence the code in (default blank).
::

    >>> code_block("This is a simple codeblock.")
    '    This is a simple codeblock.'
    >>> code_block("This is a simple codeblock.\\nBut it has a linebreak!")
    '    This is a simple codeblock.\\n    But it has a linebreak!'
    >>> code_block("This block of code has a specified language.", "python")
    '```python\\nThis block of code has a specified language.\\n```'
    >>> code_block("So\\nmany\\nlinebreaks.", "python")
    '```python\\nSo\\nmany\\nlinebreaks.\\n```'


Link
----

Return an inline link.
::

    >>> link ("This is a link", "https://github.com/abactel/markdown_strings")
    '[This is a link](https://github.com/abactel/markdown_strings)'


Image
-----

Return an inline image.

Keyword arguments:
   title -- Specify the title of the image, as seen when hovering over it.
::

    >>> image("This is an image", "https://tinyurl.com/bright-green-tree")
    '![This is an image](https://tinyurl.com/bright-green-tree)'
    >>> image("This is an image", "https://tinyurl.com/bright-green-tree", "tree")
    '![This is an image](https://tinyurl.com/bright-green-tree) "tree"'


Unordered list
--------------

Return an unordered list from an array.
::

    >>> unordered_list(["first", "second", "third", "fourth"])
    '-   first\\n-   second\\n-   third\\n-   fourth'
    >>> unordered_list([1, 2, 3, 4, 5])
    '-   1\\n-   2\\n-   3\\n-   4\\n-   5'


Ordered list
------------

Return an ordered list from an array.
::

    >>> ordered_list(["first", "second", "third", "fourth"])
    '1.  first\\n2.  second\\n3.  third\\n4.  fourth'


Blockquote
----------

Return a blockquote.
::

    >>> blockquote("A simple blockquote")
    '> A simple blockquote'


Horizontal rule
---------------

Return a horizontal rule.
::

    >>> horizontal_rule()
    '-------------------------------------------------------------------------------'


Non-standard markdown
=====================

Strikethrough
-------------

Return text with strike-through formatting.
::

    >>> strikethrough("This is a lie")
    '~This is a lie~'


Task list
---------

Return a task list.

The task_array should be 2-dimensional; the first item should be the task
text, and the second the boolean completion state.
::

    >>> task_list([["Be born", True], ["Be dead", False]])
    '- [X] Be born\\n- [ ] Be dead'

When displayed using `print`, this will appear as:
::

    - [X] Be born
    - [ ] Be dead


Table row
---------

Return a single table row.

Keyword arguments:

    pad -- The pad should be an array of the same size as the input text array.
    It will be used to format the row's padding.
::

       >>> table_row(["First column", "Second", "Third"])
       '| First column | Second | Third |'
       >>> table_row(["First column", "Second", "Third"], [10, 10, 10])
       '| First column | Second     | Third      |'


Delimiter row
-------------

Return a delimiter row for use in a table.
::

    >>> table_delimiter_row(3)
    '| --- | --- | --- |'


Table from columns
------------------

Return a formatted table, generated from arrays representing columns.

The function requires a 2-dimensional array, where each array is a column
of the table. This will be used to generate a formatted table in string
format. The number of items in each columns does not need to be consitent.
::

    >>> table_from_columns([["Name", "abactel", "Bob"], ["User", "4b4c73l", ""]])
    '| Name    | User    |\\n| ------- | ------- |\\n| abactel | 4b4c73l |\\n| Bob     |         |'

When displayed using `print`, this will appear as:
::

    | Name    | User    |
    | ------- | ------- |
    | abactel | 4b4c73l |
    | Bob     |         |


Helper functions
================

Return text with formatting escaped

Markdown requires a backslash before literal inderscores or asterisk, to avoid
formatting to bold or italics.
::

    >>> esc_format("Normal text")
    'Normal text'
    >>> esc_format("Text with **bold**")
    'Text with \\\*\\\*bold\\\*\\\*'
    >>> esc_format("Text with _italics_")
    'Text with \\\_italics\\\_'
    >>> esc_format("Text with _**complicated** formatting_")
    'Text with \\\_\\\*\\\*complicated\\\*\\\* formatting\\\_'
    """
