from src.builders.inverse_index_builder import InverseIndexBuilder
from src.index_items import TwoWordsIndexItem
from src.constants import INPUT_DIR_PATH, TWO_WORDS_INDEX_PATH


class TwoWordsIndexBuilder(InverseIndexBuilder):

    def __init__(self):
        super().__init__()

    def build(self):
        for file in self.files:
            with open(file, 'r') as f:
                file_name = file.split('/')[-1]
                lines = f.readlines()
                words = self.tokenizer.format_data(lines)
                for i in range(len(words) - 1):
                    item = (words[i], words[i+1])
                    if item not in self.index \
                        or (item in self.index
                            and self.index[item][-1].doc != file_name):
                        self.index[item] += [TwoWordsIndexItem(file_name, 1)]
                    else:
                        self.index[item][-1].count += 1


# TwoWordsIndexBuilder().run(INPUT_DIR_PATH, TWO_WORDS_INDEX_PATH)
