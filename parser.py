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
    def split_line(line: str) -> tuple:
        extra_space: int = line.find(':') + 1

        if line[extra_space] == ' ':
            line = line[:extra_space] + line[extra_space + 1:]

        key, value = line.split(':', 1)

        while value[-1] == ' ':
            value = value[:-1]
        while key[-1] == ' ':
            key = key[:-1]
        try:
            while key[0] == ' ':
                key = key[1:]
        except IndexError:
            print('=', key, '=')
        while value[0] == ' ':
            value = value[1:]

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
                    scan_active = False
                elif self.char == '#':
                    is_comment = True
                elif self.char == '\n':
                    if not line:
                        self.next()
                        continue

                    key, value = self.split_line(line)

                    result[key] = value

                    line = ""
                elif self.char not in '\t':
                    line += self.char

                self.next()
            else:
                if not is_comment:
                    if self.char == '-':
                        scan_active = True
                elif self.char == '\n':
                    is_comment = False

                    if line:
                        key, value = self.split_line(line)
                        result[key] = value

                self.next()

        return result
