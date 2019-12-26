"""markdown_strings

Markdown is a markup language with plain text formatting syntax. This package
allows the creation of markdown-compliant strings. For information about
markdown see:

-   http://commonmark.org/
-   https://daringfireball.net/projects/markdown/

"""

# Helper functions


def esc_format(text):
    """Return text with formatting escaped.

    Markdown requires a backslash before literal underscores or asterisk, to
    avoid formatting to bold or italics.

    >>> esc_format("Normal text")
    'Normal text'
    >>> esc_format("Text with **bold**") == r'Text with \\*\\*bold\\*\\*'
    True
    >>> esc_format("Text with _italics_") == r'Text with \\_italics\\_'
    True
    >>> esc_format("Text with _**complicated** format_") == r'Text with \\_\\*\\*complicated\\*\\* format\\_'
    True
    """
    return str(text).replace("_", r"\_").replace("*", r"\*")


# Standard markdown


# Emphasis


def header(header_text, header_level, style="atx"):
    """Return a header of specified level.

    Keyword arguments:
        style -- Specifies the header style (default atx).
            The "atx" style uses hash signs, and has 6 levels.
            The "setext" style uses dashes or equals signs for headers of
            levels 1 and 2 respectively, and is limited to those two levels.
            The number of dashes or equals signs is either the length
            of the text, or 3.

    Specifying a level outside of the style's range results in a ValueError.

    >>> header("Main Title", 1)
    '# Main Title'
    >>> header("Smaller subtitle", 4)
    '#### Smaller subtitle'
    >>> header("Setext style", 2, style="setext")
    'Setext style\\n------------'

    >>> header("Title", "2")
    Traceback (most recent call last):
        ...
    TypeError: header_level must be int
    >>> header(23, 1)
    Traceback (most recent call last):
        ...
    TypeError: header_text must be str
    >>> header("Title", 100)
    Traceback (most recent call last):
        ...
    ValueError: Invalid level 100 for atx
    >>> header("Title", 3, style="setext")
    Traceback (most recent call last):
        ...
    ValueError: Invalid level 3 for setext
    >>> header("Title", 1, style="asfd")
    Traceback (most recent call last):
        ...
    ValueError: Invalid style asfd (choose 'atx' or 'setext')
    """
    # check types
    if not isinstance(header_level, int):
        raise TypeError("header_level must be int")
    if not isinstance(header_text, str):
        raise TypeError("header_text must be str")
    # specifics for each style
    if style == "atx":
        if not 1 <= header_level <= 6:
            raise ValueError(f"Invalid level {header_level} for atx")
        return f"{'#' * header_level} {esc_format(header_text)}"
    elif style == "setext":
        if not 0 < header_level < 3:
            raise ValueError(f"Invalid level {header_level} for setext")
        header_character = "=" if header_level == 1 else "-"
        header_string = (header_character * 3) + header_character * (len(header_text) - 3)
        return f"{esc_format(header_text)}\n{header_string}"
    else:
        raise ValueError(f"Invalid style {style} (choose 'atx' or 'setext')")


def italics(text):
    """Return italics formatted text.

    >>> italics("This text is italics") == '_This text is italics_'
    True
    >>> italics("A wild _underscore_ appears") == r'_A wild \\_underscore\\_ appears_'
    True
    """
    return f"_{esc_format(text)}_"


def bold(text):
    """Return bold formatted text.

    >>> bold("This text is bold")
    '**This text is bold**'
    >>> bold("Oh look, **stars** everywhere") == r'**Oh look, \\*\\*stars\\*\\* everywhere**'
    True
    """
    return f"**{esc_format(text)}**"


# Code formatting


def inline_code(text):
    """Return formatted inline code.

    >>> inline_code("This text is code")
    '`This text is code`'
    """
    return f"`{str(text)}`"


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
        return f"```{language}\n{text}\n```"
    return "\n".join([f"    {item}" for item in text.split("\n")])


# Links


def link(text, link_url):
    """Return an inline link.

    >>> link ("This is a link", "https://github.com/awesmubarak/markdown_strings")
    '[This is a link](https://github.com/awesmubarak/markdown_strings)'
    """
    return f"[{esc_format(text)}]({link_url})"


def image(alt_text, link_url, title=""):
    """Return an inline image.

    Keyword arguments:
    title -- Specify the title of the image, as seen when hovering over it.

    >>> image("This is an image", "https://avatars3.githubusercontent.com/u/24862378")
    '![This is an image](https://avatars3.githubusercontent.com/u/24862378)'
    >>> image("This is an image", "https://avatars3.githubusercontent.com/u/24862378", "awes")
    '![This is an image](https://avatars3.githubusercontent.com/u/24862378) "awes"'
    """
    image_string = f"![{esc_format(alt_text)}]({link_url})"
    if title:
        image_string += f' "{esc_format(title)}"'
    return image_string


# Lists


def unordered_list(text_list):
    """Return an unordered list from an list.

    >>> unordered_list(["first", "second", "third", "fourth"])
    '-   first\\n-   second\\n-   third\\n-   fourth'
    >>> unordered_list([1, 2, 3, 4, 5])
    '-   1\\n-   2\\n-   3\\n-   4\\n-   5'
    """
    return "\n".join([f"-   {esc_format(item)}" for item in text_list])


def ordered_list(text_list):
    """Return an ordered list from an list.

    >>> ordered_list(["first", "second", "third", "fourth"])
    '1.  first\\n2.  second\\n3.  third\\n4.  fourth'
    """
    ordered_list = []
    for number, item in enumerate(text_list):
        ordered_list.append(
            f"{(f'{esc_format(number + 1)}.').ljust(3)} {esc_format(item)}"
        )
    return "\n".join(ordered_list)


# Miscellaneous


def blockquote(text):
    """Return a blockquote.

    >>> blockquote("A simple blockquote")
    '> A simple blockquote'
    """
    return "\n".join([f"> {esc_format(item)}" for item in text.split("\n")])


def horizontal_rule(length=79, style="_"):
    """Return a horizontal rule.

    Keyword arguments:
        length -- Specifies the length of the rule (default 79, minimum 3).
        style -- Character used for the rule (may be either "_" or "*").

    If the length is too low, or the style is invalid, a ValueError is raised.

    >>> horizontal_rule()
    '_______________________________________________________________________________'
    >>> horizontal_rule(length=5, style="*")
    '*****'

    >>> horizontal_rule(style="=")
    Traceback (most recent call last):
        ...
    ValueError: Invalid style (choose '_' or '*')
    >>> horizontal_rule(length=2)
    Traceback (most recent call last):
        ...
    ValueError: Length must be >= 3

    """
    if style not in ("_", "*"):
        raise ValueError("Invalid style (choose '_' or '*')")
    if length < 3:
        raise ValueError("Length must be >= 3")
    return style * length


# Non-standard markdown


def strikethrough(text):
    """Return text with strike-through formatting.

    >>> strikethrough("This is a lie")
    '~This is a lie~'
    """
    return f"~{esc_format(text)}~"


def task_list(task_list):
    """Return a task list.

    The task_list should be 2-dimensional; the first item should be the task
    text, and the second the boolean completion state.

    >>> task_list([["Be born", True], ["Be dead", False]])
    '- [X] Be born\\n- [ ] Be dead'

    When displayed using `print`, this will appear as:

        - [X] Be born
        - [ ] Be dead
    """
    tasks = []
    for item, completed in task_list:
        tasks.append(f"- [{'X' if completed else ' '}] {esc_format(item)}")
    return "\n".join(tasks)


# Tables


def table_row(text_list, pad=-1):
    """Return a single table row.
    Keyword arguments:
    pad -- The pad should be an list of the same size as the input text list.æ
           It will be used to format the row's padding.

    >>> table_row(["First column", "Second", "Third"])
    '| First column | Second | Third |'
    >>> table_row(["First column", "Second", "Third"], [10, 10, 10])
    '| First column | Second     | Third      |'
    """
    if pad == -1:
        pad = [0] * len(text_list)
    row = "|"
    for column_number in range(len(text_list)):
        padding = pad[column_number] + 1
        row += (" " + esc_format(text_list[column_number])).ljust(padding) + " |"
    return row


def table_delimiter_row(number_of_columns, column_lengths=-1):
    """Return a delimiter row for use in a table.
    Keyword arguments:
    column_lengths -- An iterable that specifies the length of each column.

    >>> table_delimiter_row(3)
    '| --- | --- | --- |'
    >>> table_delimiter_row(3, column_lengths=[4,5,6])
    '| ---- | ----- | ------ |'

    >>> table_delimiter_row(3, column_lengths=[1,2])
    Traceback (most recent call last):
        ...
    ValueError: number_of_columns must be the number of columns in column_lengths
    """
    if column_lengths == -1:
        column_lengths = [0] * number_of_columns
    # error checking
    if number_of_columns != len(column_lengths):
        raise ValueError("number_of_columns must be the number of columns in column_lengths")
    # creating the list with the right number of dashes
    delimiter_row = []
    for column_number in range(0, number_of_columns):
        delimiter_row.append("---" + "-" * (column_lengths[column_number] - 3))
    # use table row for acctually creating the table row
    return table_row(delimiter_row)


def table(table_list):
    """Return a formatted table, generated from lists representing columns.
    The function requires a 2-dimensional list, where each list is a column
    of the table. This will be used to generate a formatted table in string
    format. The number of items in each columns does not need to be consitent.

    >>> table([["1","2","3"], ["4","5","6"], ["7","8","9"]])
    '| 1 | 4 | 7 |\\n| --- | --- | --- |\\n| 2 | 5 | 8 |\\n| 3 | 6 | 9 |'

    >>> table([["Name", "Awes", "Bob"], ["User", "mub123", ""]])
    '| Name | User   |\\n| ---- | ------ |\\n| Awes | mub123 |\\n| Bob  |        |'
    """
    number_of_columns = len(table_list)
    number_of_rows_in_column = [len(column) for column in table_list]
    string_list = [[str(cell) for cell in column] for column in table_list] # so cell can be int
    column_lengths = [len(max(column, key=len)) for column in string_list]
    table = []

    # title row
    row_list = [column[0] for column in string_list]
    table.append(table_row(row_list, pad=column_lengths))

    # delimiter row
    table.append(table_delimiter_row(len(column_lengths), column_lengths=column_lengths))

    # body rows
    for row in range(1, max(number_of_rows_in_column)):
        row_list = []
        for column_number in range(number_of_columns):
            if number_of_rows_in_column[column_number] > row:
                row_list.append(string_list[column_number][row])
            else:
                row_list.append("")
        table.append(table_row(row_list, pad=column_lengths))
    return "\n".join(table)


def table_from_rows(table_list):
    """Return a formatted table, using each list as the list. The specifics are
    the same as those for the table function.

    >>> table_from_rows([["1","2","3"],["4","5","6"],["7","8","9"]])
    '| 1 | 2 | 3 |\\n| --- | --- | --- |\\n| 4 | 5 | 6 |\\n| 7 | 8 | 9 |'
    """
    # transpose the list
    number_of_rows = len(table_list)
    transposed = []
    for column_number in range(0, number_of_rows):
        column_list = [row[column_number] for row in table_list]
        transposed.append(column_list)

    return table(transposed)
