class Parser:
    def __init__(self, source: str):
        self.source: str = source
        self.index: int = -1
        self.char: str = None
        self.next()
        
    def next(self) -> None:
        "Advance to the next character in the source text if not at end, else sets char to None."
        self.index += 1
        self.char = self.source[self.index] if self.index < len(self.source) else None
        
    def parse(self, text: str) -> dict:
        """
        Returns a Python dictionary from the inputted QuickInfo text.
        :param str text:
        """
        file_start: bool = False
        
        pair_list: list = []
        
        pair_string: str = ""
        
        result: dict = {}
        
        while self.char is not None:
            if self.char not in '\t':
                if self.char == '\n':
                    pair_list.append(pair_string)
                    pair_string = ""
                    
                pair_string += self.char
        
        for item: str in pair_list:
            extra_space: int = item.find(':') + 1
            
            if extra_space == ' ':
                item = item[:extra_space] + item[extra_space + 1:]
                
            key: str, value: str = item.split(':')
            
            result[key] = value
            
        return result
