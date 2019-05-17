import csv

from collections import defaultdict

from src.builders.base_builder import BaseBuilder
from src.tokenizer import Tokenizer


class BaseIndexBuilder(BaseBuilder):

    def __init__(self):
        super().__init__()
        self.tokenizer = Tokenizer()
        self.index = defaultdict(list)

    def save(self, output_path):
        field_names = ['Token', 'Docs']
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(field_names)

            for k, v in self.index.items():
                writer.writerow([k, ' -> '.join(map(lambda x: x.__str__(), v))])
