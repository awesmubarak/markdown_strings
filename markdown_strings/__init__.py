"""markdown_strings

Markdown is a markup language with plain text formatting syntax. This package
allows the creation of markdown-compliant strings. For information about
markdown see:

-   http://commonmark.org/
-   https://daringfireball.net/projects/markdown/

"""

# Helper functions


def esc_format(text):
    """Return text with formatting escaped

    Markdown requires a backslash before literal inderscores or asterisk, to
    avoid formatting to bold or italics.

    >>> esc_format("Normal text")
    'Normal text'
    >>> esc_format("Text with **bold**")
    'Text with \\\*\\\*bold\\\*\\\*'
    >>> esc_format("Text with _italics_")
    'Text with \\\_italics\\\_'
    >>> esc_format("Text with _**complicated** formatting_")
    'Text with \\\_\\\*\\\*complicated\\\*\\\* formatting\\\_'
    """
    return str(text).replace("_", "\_").replace("*", "\*")


# Standard markdown


# Emphasis


def header(heading_text, header_level):
    """Return a header of specified level.

    >>> header("Main Title", 1)
    '# Main Title'
    >>> header("Smaller subtitle", 4)
    '#### Smaller subtitle'
    """
    return(("#" * header_level) + " " + esc_format(heading_text))


def italics(text):
    """Return italics formatted text.

    >>> italics("This text is italics")
    '_This text is italics_'
    >>> italics("A wild _underscore_ appears")
    '_A wild \\\_underscore\\\_ appears_'
    """
    return("_" + esc_format(text) + "_")


def bold(text):
    """Return bold formatted text.

    >>> bold("This text is bold")
    '**This text is bold**'
    >>> bold("Oh look, **stars** everywhere")
    '**Oh look, \\\*\\\*stars\\\*\\\* everywhere**'
    """
    return("**" + esc_format(text) + "**")


# Code formatting


def inline_code(text):
    """Return formatted inline code.

    >>> inline_code("This text is code")
    '`This text is code`'
    """
    return("`" + str(text) + "`")


def code_block(text, language=""):
    """Return a code block.

    If a language is specified a fenced code block is produced, otherwise the
    block is indented by four spaces.

    Keyword arguments:
    language -- Specifies the language to fence the code in (default blank).

    >>> code_block("This is a simple codeblock.")
    '    This is a simple codeblock.'
    >>> code_block("This is a simple codeblock.\\nBut it has a linebreak!")
    '    This is a simple codeblock.\\n    But it has a linebreak!'
    >>> code_block("This block of code has a specified language.", "python")
    '```python\\nThis block of code has a specified language.\\n```'
    >>> code_block("So\\nmany\\nlinebreaks.", "python")
    '```python\\nSo\\nmany\\nlinebreaks.\\n```'
    """
    if language:
        return("```" + language + "\n" + text + "\n```")
    else:
        return("\n".join(["    " + item for item in text.split("\n")]))


# Links

def link(text, link):
    """Return an inline link.

    >>> link ("This is a link", "https://github.com/abactel/markdown_strings")
    '[This is a link](https://github.com/abactel/markdown_strings)'
    """
    return("[" + esc_format(text) + "](" + link + ")")


def image(alt_text, link, title=""):
    """Return an inline image.

    Keyword arguments:
    title -- Specify the title of the image, as seen when hovering over it.

    >>> image("This is an image", "https://tinyurl.com/bright-green-tree")
    '![This is an image](https://tinyurl.com/bright-green-tree)'
    >>> image("This is an image", "https://tinyurl.com/bright-green-tree", "tree")
    '![This is an image](https://tinyurl.com/bright-green-tree) "tree"'
    """
    image_string = "![" + esc_format(alt_text) + "](" + link + ")"
    if title:
        image_string += ' "' + esc_format(title) + '"'
    return(image_string)


# Lists


def unordered_list(text_array):
    """Return an unordered list from an array.

    >>> unordered_list(["first", "second", "third", "fourth"])
    '-   first\\n-   second\\n-   third\\n-   fourth'
    >>> unordered_list([1, 2, 3, 4, 5])
    '-   1\\n-   2\\n-   3\\n-   4\\n-   5'
    """
    return("\n".join([("-   " + esc_format(item)) for item in text_array]))


def ordered_list(text_array):
    """Return an ordered list from an array.

    >>> ordered_list(["first", "second", "third", "fourth"])
    '1.  first\\n2.  second\\n3.  third\\n4.  fourth'
    """
    text_list = []
    for number, item in enumerate(text_array):
        text_list.append((esc_format(number + 1) + ".").ljust(3)
                         + " " + esc_format(item))
    return("\n".join(text_list))


# Miscellaneous


def blockquote(text):
    """Return a blockquote.

    >>> blockquote("A simple blockquote")
    '> A simple blockquote'
    """
    return("\n".join(["> " + esc_format(item) for item in text.split("\n")]))


def horizontal_rule():
    """Return a horizontal rule.

    >>> horizontal_rule()
    '-------------------------------------------------------------------------------'
    """
    return("-" * 79)


# Non-standard markdown


def strikethrough(text):
    """Return text with strike-through formatting.

    >>> strikethrough("This is a lie")
    '~This is a lie~'
    """
    return("~" + esc_format(text) + "~")


def task_list(task_array):
    """Return a task list.

    The task_array should be 2-dimensional; the first item should be the task
    text, and the second the boolean completion state.

    >>> task_list([["Be born", True], ["Be dead", False]])
    '- [X] Be born\\n- [ ] Be dead'

    When displayed using `print`, this will appear as:

        - [X] Be born
        - [ ] Be dead
    """
    task_list = []
    for item, completed in task_array:
        task = "- [ ] " + esc_format(item)
        if completed:
            task = task[:3] + "X" + task[4:]
        task_list.append(task)
    return("\n".join(task_list))


# Tables


def table_row(text_array, pad=-1):
    """Return a single table row.

    Keyword arguments:
    pad -- The pad should be an array of the same size as the input text array.
           It will be used to format the row's padding.

    >>> table_row(["First column", "Second", "Third"])
    '| First column | Second | Third |'
    >>> table_row(["First column", "Second", "Third"], [10, 10, 10])
    '| First column | Second     | Third      |'
    """
    if pad == -1:
        pad = ([0] * len(text_array))
    row = "|"
    for column_number in range(len(text_array)):
        padding = pad[column_number] + 1
        row += ((" " + esc_format(text_array[column_number])).ljust(padding) + " |")
    return(row)


def table_delimiter_row(number_of_columns):
    """Return a delimiter row for use in a table.

    >>> table_delimiter_row(3)
    '| --- | --- | --- |'
    """
    return(table_row(["---" for column in range(number_of_columns)]))


def table(big_array):
    """Return a formatted table, generated from arrays representing columns.

    The function requires a 2-dimensional array, where each array is a column
    of the table. This will be used to generate a formatted table in string
    format. The number of items in each columns does not need to be consitent.

    >>> table([["Name", "abactel", "Bob"], ["User", "4b4c73l", ""]])
    '| Name    | User    |\\n| ------- | ------- |\\n| abactel | 4b4c73l |\\n| Bob     |         |'

    When displayed using `print`, this will appear:

        | Name    | User    |
        | ------- | ------- |
        | abactel | 4b4c73l |
        | Bob     |         |
    """
    number_of_columns = len(big_array)
    number_of_rows_in_column = [len(column) for column in big_array]
    max_cell_size = [len(max(column, key=len)) for column in big_array]
    table = []

    # title row
    row_array = [column[0] for column in big_array]
    table.append(table_row(row_array, pad=max_cell_size))

    # delimiter row
    row_array = []
    for column_number in range(number_of_columns):
        row_array.append("-" * max_cell_size[column_number])
    table.append(table_row(row_array, pad=max_cell_size))

    # body rows
    for row in range(1, max(number_of_rows_in_column)):
        row_array = []
        for column_number in range(number_of_columns):
            if number_of_rows_in_column[column_number] > row:
                row_array.append(big_array[column_number][row])
            else:
                row_array.append()
        table.append(table_row(row_array, pad=max_cell_size))
    return("\n".join(table))
