from src.builders.base_index_builder import BaseIndexBuilder
from src.index_items import InverseIndexItem
from src.constants import INPUT_DIR_PATH, INVERSE_INDEX_PATH


class InverseIndexBuilder(BaseIndexBuilder):

    def __init__(self):
        super().__init__()

    def run(self, input_dir_path, output_path):
        self.build_index(input_dir_path)
        self.save(output_path)

    def build_index(self, input_dir_path):
        self.load_files(input_dir_path)
        self.build()
        self.sort_index()
        return self.index

    def sort_index(self):
        for k, v in self.index.items():
            self.index[k] = sorted(v, key=lambda x: x.count)

    def build(self):
        for file in self.files:
            with open(file, 'r') as f:
                file_name = file.split('/')[-1]
                lines = f.readlines()
                words = self.tokenizer.format_data(lines)
                for word in words:
                    if word not in self.index \
                        or (word in self.index
                            and self.index[word][-1].doc != file_name):
                        self.index[word] += [InverseIndexItem(file_name, 1)]
                    else:
                        self.index[word][-1].count += 1


InverseIndexBuilder().run(INPUT_DIR_PATH, INVERSE_INDEX_PATH)
