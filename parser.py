from error_handling import *


class Parser:
    def __init__(self, source: str):
        self._source: str = source
        self._index: int = -1
        self._line_number = 0
        self._line_character_index = -1
        self._char: str = ""
        self._next()

    def get_index(self):
        return self._index

    def get_line_number(self):
        return self._line_number

    def get_line_character_index(self):
        return self._line_character_index

    def get_source(self):
        return self._source

    def get_current_char(self):
        return self._char

    def _get_relative_position(self):
        return self._line_number, self._line_character_index

    def _next(self) -> None:
        """
        Advance to the next character in the source text if not at end, else sets char to None.

        Updates the relative indices for error feedback.
        :return:
        """

        self._index += 1

        if self._char == '\n':
            self._line_number += 1
            self._line_character_index = 1
        else:
            self._line_character_index += 1

        self._char = self._source[self._index] if self._index < len(self._source) else '\0'

    @staticmethod
    def _cast_if_number(string: str):
        """
        Checks if the string value passed in is an integer or float; if it is, it converts it to the Python type.
        If the value is a string, it returns the original string.
        :param string:
        :return:
        """
        is_int: bool = False
        is_float: bool = False

        try:
            float(string)
            is_float = True
            try:
                int(string)
                is_int = True
                is_float = False
            except ValueError:
                is_int = False
        except ValueError:
            is_int = False

        if is_int:
            return int(string)
        elif is_float:
            return float(string)
        else:
            return string

    def check_if_number(self, value):
        casted_value = self._cast_if_number(value)

        if isinstance(casted_value, int) or isinstance(casted_value, float):
            return casted_value

        if casted_value[0] == "'":
            casted_value_new = self._cast_if_number(casted_value[1:])

            if not isinstance(casted_value_new, str):
                return casted_value[1:]
        else:
            return value

    def _split_line(self, line: str) -> ParseResult:
        key, value = line.split(':', 1)

        key = key.strip()
        value = value.strip()

        value = self.check_if_number(value)

        return ParseResult((key, value))

    def _parse_list(self, string):
        """
        Parses any values that are of a 'list' type.
        :param string:
        :return: A Python list formed by the string, passes an error if unable to parse.
        """
        result_list = []
        stack = []
        str_buffer = ""

        for char in string:
            if char == '/':
                # Add a new level of nesting to the stack.
                # Check if comma is missing before starting a new nested list.
                if len(str_buffer.replace(' ', '')) > 0:
                    return ParseResult(
                        None,
                        ListError(
                            self._get_relative_position(),
                            "Possible mismatched list brackets"
                        )
                    )

                stack.append([])

            elif char == '\\':
                # Combine the temporary list and the global list, pop the current context off the stack.
                try:
                    current_level = stack.pop()
                except IndexError:
                    return ParseResult(
                        None,
                        ListError(
                            self._get_relative_position(),
                            "Extra closing list brackets found"
                        )
                    )

                if len(str_buffer.replace(' ', '')) > 0:
                    current_level.append(self.check_if_number(str_buffer.strip()))
                    str_buffer = ""

                if len(result_list) == 0:
                    result_list = current_level
                else:
                    sublist = current_level

                    if sublist is not None:
                        sublist.append(result_list)
                        result_list = sublist
            else:
                # Check if there are more elements than closing brackets
                try:
                    sublist = stack.pop()
                except IndexError:
                    return ParseResult(
                        None,
                        ListError(
                            self._get_relative_position(),
                            "Missing closing bracket or elements defined outside list bounds"
                        )
                    )

                if char != ',':
                    str_buffer += char
                else:
                    sublist.append(self.check_if_number(str_buffer.strip()))
                    str_buffer = ""

                stack.append(sublist)

        if len(stack) != 0:
            # If the stack is not empty after the loop, then there may be missing closing brackets.
            return ParseResult(
                None,
                ListError(
                    self._get_relative_position(),
                    "List brackets may be mismatched (missing closing bracket)"
                )
            )

        return ParseResult(result_list)

    def _main_parser(self, line) -> ParseResult:
        """
        Handles parsing internal to the "document".
        :param line:
        :return:
        """
        try:
            # Attempt to split into key-value pairs.
            split_result = self._split_line(line)

            split_data, split_error = split_result

            if split_error:
                return split_result

            key, value = split_data

            if isinstance(value, str):
                final_list: list = []

                # If the value is of a 'list' type, then parse as a list.
                if value[0] == '/':
                    list_parse_result = self._parse_list(value)

                    parse_data, parse_error = list_parse_result

                    if parse_error:
                        return list_parse_result

                    value = parse_data

                # Return error if quotes used in input
                if '"' in value:
                    return ParseResult(
                        None,
                        InvalidCharacterError(
                            self._get_relative_position(),
                            "You have passed in an invalid character in the input."
                        )
                    )

            return ParseResult((key, value))

        except (ValueError, IndexError):
            return ParseResult(
                None,
                MismatchedKeyValueError(
                    self._get_relative_position(),
                    "Missing value or key in file"
                )
            )

    def parse(self) -> dict:
        """
        Parses the text based on the grammar rules.

        :return: Python dictionary.
        """

        scan_active: bool = False
        is_comment: bool = False
        start_of_line: bool = False

        line: str = ""
        result: dict = {}

        while self._char != '\0':
            if scan_active and not is_comment:
                if self._char == '-':
                    self._next()
                    if self._char == '\n':
                        scan_active = False
                    else:
                        line += f'-{self._char}'
                elif self._char == '#':
                    is_comment = True
                elif self._char == '\n':
                    if not line:
                        self._next()
                        continue

                    main_parser_result = self._main_parser(line)

                    main_data, main_error = main_parser_result

                    if main_error:
                        main_error.print_error()
                        return {}

                    key, value = main_data

                    if key in result.keys():
                        DuplicateKeyError(
                            self._get_relative_position(),
                            "A dictionary key must be unique."
                        ).print_error()

                        return {}

                    result[key] = value

                    line = ""
                elif self._char not in '\t':
                    line += self._char

                self._next()

                # Check if the document has ended before encountering the closing dash.
                if self._char == '\0':
                    if scan_active:
                        DocumentBoundaryError(
                            self._get_relative_position(),
                            "The file start or end marker '-' is missing."
                        ).print_error()
            else:
                # Check if starting '-' dash found, if so, start the document parsing.
                if not is_comment:
                    if self._char == '-' and not line:
                        scan_active = True

                    # Parse the rest of the line as a comment.
                    if self._char == '#':
                        is_comment = True

                # Disable comment toggle when new line is reached.
                elif self._char == '\n':
                    is_comment = False

                    main_parser_result = self._main_parser(line)

                    main_data, main_error = main_parser_result

                    if main_error:
                        main_error.print_error()
                        return {}

                    key, value = main_data

                    result[key] = value
                    line = ""

                self._next()

        if not result:
            DocumentBoundaryError(
                self._get_relative_position(),
                "The file start or end marker '-' is missing."
            ).print_error()
            return {}

        return result
