class Parser:
    def __init__(self, source: str):
        self._source: str = source
        self._index: int = -1
        self._char: str = ""
        self._next()

    def get_index(self):
        return self._index

    def get_source(self):
        return self._source

    def get_current_char(self):
        return self._char

    def _next(self) -> None:
        "Advance to the next character in the source text if not at end, else sets char to None."
        self._index += 1
        self._char = self._source[self._index] if self._index < len(self._source) else None

    @staticmethod
    def _check_if_number(string_value: str):
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

    def _split_line(self, line: str) -> tuple:
        key, value = line.split(':', 1)

        key = key.strip()
        value = value.strip()

        casted_value = self._check_if_number(value)

        if casted_value:
            value = casted_value

        return key, value

    def _main_parser(self, line):
        try:
            key, value = self._split_line(line)

            if isinstance(value, str):
                final_list: list = []
                if value[0] == '/':
                    modif_val: str = value[1:]

                    end_index: int = modif_val.find('/')

                    if end_index == -1:
                        print("Missing closing symbol for list")
                        return {}

                    modif_val = modif_val[:end_index]

                    modif_values: list = modif_val.split(',')

                    final_list = [k.strip() for k in modif_values]

                    for idx, item in enumerate(final_list):
                        casted_num: int = self._check_if_number(item)
                        if casted_num:
                            final_list[idx] = casted_num

                    value = final_list

            return key, value

        except (ValueError, IndexError):
            print("Missing value or key in file")
            return None

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

        while self._char is not None:
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

                    key, value = self._main_parser(line)

                    if not value:
                        return {}

                    result[key] = value

                    line = ""
                elif self._char not in '\t':
                    line += self._char

                self._next()
            else:
                if not is_comment:
                    if self._char == '-' and not line:
                        scan_active = True
                    if self._char == '#':
                        is_comment = True
                elif self._char == '\n':
                    is_comment = False

                    if line:
                        key, value = self._main_parser(line)

                        if not value:
                            return {}

                        result[key] = value
                        line = ""

                self._next()

        if not result:
            print("File start marker missing")
            return {}

        return result
