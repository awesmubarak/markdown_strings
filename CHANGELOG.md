# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## Unreleased

### Added

-   New flag to prevent escaping, `esc`

## [3.3.0] - 2019-12-26

### Added

-   The keyword argument `column_lengths` for `table_delimiter_row` allows the
    length of each column to be specified.

## [3.2.0] - 2019-12-26

### Added

-   `table_from_rows` creates tables from lists containing each row

## Changed

-   Columns of the table can contain non-strings
-   The setex header's heading characters are now the same length as the heading text.

[3.3.0]: https://github.com/awesmubarak/gitget/compare/v3.2.0...v3.3.0
[3.2.0]: https://github.com/awesmubarak/gitget/releases/tag/v3.2.0
