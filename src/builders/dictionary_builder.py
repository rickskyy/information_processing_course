from src.builders.base_builder import BaseBuilder
from src.tokenizer import Tokenizer
# from src.constants import DICT_PATH, INPUT_DIR_PATH


class DictionaryBuilder(BaseBuilder):

    def __init__(self):
        super().__init__()
        self.dictionary = set()
        self.count = 0
        self.tokenizer = Tokenizer()

    def run(self, input_dir_path, output_path):
        self.load_files(input_dir_path)
        self.build()
        self.save(output_path)
        self.print_counts()

    def build(self):
        for file in self.files:
            with open(file, 'r') as f:
                lines = f.readlines()
                words = self.tokenizer.format_data(lines)
                self.count += len(words)
                self.dictionary.update(words)

    def save(self, output_path):
        with open(output_path, 'w') as f:
            f.write('\n'.join(sorted(self.dictionary)))

    def print_counts(self):
        print('Total count: ', self.count)
        print('Dictionary count: ', len(self.dictionary))


# DictionaryBuilder().run(INPUT_DIR_PATH, DICT_PATH)
