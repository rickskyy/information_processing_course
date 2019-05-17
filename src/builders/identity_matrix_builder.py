import csv

from src.builders.base_builder import BaseBuilder
from src.tokenizer import Tokenizer
from src.constants import INPUT_DIR_PATH, IDENTITY_MATRIX_PATH, DICT_PATH


class IdentityMatrixBuilder(BaseBuilder):

    def __init__(self, dict_path):
        super().__init__()
        self.dict_path = dict_path
        self.dictionary = set()
        self.matrix = {}
        self.tokenizer = Tokenizer()

    def run(self, input_dir_path, output_path):
        self.load_dictionary()
        self.load_files(input_dir_path)
        self.init_matrix()
        self.build()
        self.save(output_path)

    def load_dictionary(self):
        with open(self.dict_path, 'r') as f:
            lines = self.tokenizer.filter_new_lines(f.readlines())
            self.dictionary = sorted(lines)

    def init_matrix(self):
        self.matrix = {
            x: [0]*len(self.files) for x in self.dictionary
        }

    def build(self):
        for i, file in enumerate(self.files):
            with open(file, 'r') as f:
                lines = f.readlines()
                words = self.tokenizer.format_data(lines)
                for word in words:
                    self.matrix[word][i] += 1

    def save(self, output_path):
        field_names = ['Token'] + list(map(lambda x: x.split('/')[-1], self.files))
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(field_names)

            for k, v in self.matrix.items():
                writer.writerow([k] + v)


# IdentityMatrixBuilder(DICT_PATH).run(INPUT_DIR_PATH, IDENTITY_MATRIX_PATH)
