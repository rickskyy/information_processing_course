import re


class Tokenizer:
    REGEX = re.compile(r'[^a-zA-Z\s+]')
    WHITE_SPACES = re.compile(r'\s+')

    def format_data(self, lines):
        _list = []
        for line in lines:
            line = self.REGEX.sub('', line).strip()
            line = self.WHITE_SPACES.sub(' ', line)
            words = filter(lambda x: x, line.split(' '))
            words = list(map(lambda x: x.lower(), words))
            _list.extend(words)

        return _list

    def filter_new_lines(self, _list):
        return list(map(lambda x: self.WHITE_SPACES.sub('', x), _list))
