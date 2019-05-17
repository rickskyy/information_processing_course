from src.builders.base_index_builder import BaseIndexBuilder
from src.index_items import CoordinateIndexItem
from src.constants import INPUT_DIR_PATH, COORDINATE_INDEX_PATH
from src.utils import get_split_file_path_by_name


class CoordinateIndexBuilder(BaseIndexBuilder):

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
            self.index[k] = sorted(v, key=lambda x: x.count, reverse=True)

    def build(self):
        for file in self.files:
            with open(file, 'r') as f:
                file_name = file.split('/')[-1]
                lines = f.readlines()
                words = self.tokenizer.format_data(lines)
                for i in range(len(words)):
                    item = words[i]
                    if item not in self.index \
                        or (item in self.index
                            and self.index[item][-1].doc != file_name):
                        self.index[item] += [
                            CoordinateIndexItem(file_name, 1, [i])
                        ]
                    else:
                        self.index[item][-1].count += 1
                        self.index[item][-1].coordinates.append(i)

    def show_nearby(self, doc, word_indexes_list):
        file = get_split_file_path_by_name(doc)
        res = []
        with open(file, 'r') as f:
            lines = f.readlines()
            words = self.tokenizer.format_data(lines)
            for word_index in word_indexes_list:
                start = word_index - 10 if word_index - 10 >= 0 else 0
                end = word_index + 10
                res.append(' '.join(words[start:end]))
        return res


# CoordinateIndexBuilder().run(INPUT_DIR_PATH, COORDINATE_INDEX_PATH)
