class ParseResult:
    """
    Each parse operation involving a potential failed result is wrapped in a ParseResult in order to detect and pass
    any errors back to the main parse function.
    """

    def __init__(self, result, error=None):
        self.result = result
        self.error = error

    def __iter__(self):
        yield self.result
        yield self.error


class ParserError:
    """
    Base class of custom errors relating to the parsing process.
    """

    def __init__(self, current_position, details):
        line, column = current_position
        self.message = f"{type(self).__name__}: {details} | [ line {line}, col {column} ]"

    def error_message_as_string(self):
        return self.message

    def print_error(self):
        print(self.message)


class ListError(ParserError):
    """
    Errors involving list operations or general formatting.
    """

    def __init__(self, current_position, details):
        super().__init__(current_position, details)


class NotANumberError(ParserError):
    """
    Errors relating to invalid numbers or characters.
    """

    def __init__(self, current_position, details):
        super().__init__(current_position, details)


class MismatchedKeyValueError(ParserError):
    """
    Errors relating to a missing key / missing value.
    """

    def __init__(self, current_position, details):
        super().__init__(current_position, details)


class DuplicateKeyError(ParserError):
    """
    Errors relating to a duplicate key.
    """

    def __init__(self, current_position, details):
        super().__init__(current_position, details)


class DocumentBoundaryError(ParserError):
    """
    Errors involving the invalid parsing of the document boundaries.
    """

    def __init__(self, current_position, details):
        super().__init__(current_position, details)


class KeyValueParseError(ParserError):
    """
    Errors involving the parsing of the key-value strings into Python objects.
    """

    def __init__(self, current_position, details):
        super().__init__(current_position, details)


class InvalidCharacterError(ParserError):
    """
    Invalid character in input.
    """

    def __init__(self, current_position, details):
        super().__init__(current_position, details)