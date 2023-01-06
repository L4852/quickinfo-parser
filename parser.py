class Parser:
    def __init__(self, source: str):
        self.source: str = source
        self.index: int = -1
        self.char: str = ""
        self.next()

    def next(self) -> None:
        "Advance to the next character in the source text if not at end, else sets char to None."
        self.index += 1
        self.char = self.source[self.index] if self.index < len(self.source) else None

    @staticmethod
    def check_number(string_value: str):
        is_int: bool = False
        is_float: bool = False

        try:
            float(string_value)
            is_float = True
            try:
                int(string_value)
                is_int = True
                is_float = False
            except ValueError:
                is_int = False
        except ValueError:
            is_int = False

        if is_int:
            return int(string_value)
        elif is_float:
            return float(string_value)
        else:
            return None

    @staticmethod
    def split_line(line: str) -> tuple:
        extra_space: int = line.find(':') + 1

        if line[extra_space] == ' ':
            line = line[:extra_space] + line[extra_space + 1:]

        key, value = line.split(':', 1)

        while value[-1] == ' ':
            value = value[:-1]
        while key[-1] == ' ':
            key = key[:-1]
        while key[0] == ' ':
            key = key[1:]
        while value[0] == ' ':
            value = value[1:]

        casted_value = Parser.check_number(value)

        if casted_value:
            value = casted_value

        return key, value

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

        while self.char is not None:
            if scan_active and not is_comment:
                if self.char == '-':
                    self.next()
                    if self.char == '\n':
                        scan_active = False
                    else:
                        line += f'-{self.char}'
                elif self.char == '#':
                    is_comment = True
                elif self.char == '\n':
                    if not line:
                        self.next()
                        continue

                    try:
                        key, value = self.split_line(line)
                    except (ValueError, IndexError):
                        print("Missing value or key in file")
                        return {}

                    result[key] = value

                    line = ""
                elif self.char not in '\t':
                    line += self.char

                self.next()
            else:
                if not is_comment:
                    if self.char == '-' and not line:
                        scan_active = True
                    if self.char == '#':
                        is_comment = True
                elif self.char == '\n':
                    is_comment = False

                    if line:
                        key, value = self.split_line(line)
                        result[key] = value
                        line = ""

                self.next()

        if not result:
            print("File start marker missing")
            return {}

        return result
