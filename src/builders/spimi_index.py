import sys
import csv
import json

from collections import defaultdict, namedtuple
from functools import reduce

from src.builders.base_index_builder import BaseIndexBuilder
from src.index_items import InverseIndexItem
from src.constants import (
    INPUT_DIR_PATH,
    SPIMI_INDEX_BLOCKS_PATH,
    SPIMI_INDEX_PATH
)


TermItem = namedtuple('Item', ['term', 'postings_list'])


class SPIMIIndexBuilder(BaseIndexBuilder):

    BLOCK_SIZE_LIMIT = 200_000

    def __init__(self):
        super().__init__()
        self.blocks = []

    def run(self, input_dir_path):
        self.build_index(input_dir_path)

    def build_index(self, input_dir_path):
        self.load_files(input_dir_path)
        self.build_blocks()
        self.load_blocks()
        self.merge_blocks()

    def build_blocks(self):
        block_number = 0
        for file_idx, file in enumerate(self.files):
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

            if sys.getsizeof(self.index) > self.BLOCK_SIZE_LIMIT \
                    or (file_idx == len(self.files) - 1):
                terms_index_list = self._get_sorted_index_terms_list(self.index)
                self._save_block(block_number, terms_index_list)
                self.index = defaultdict(list)
                block_number += 1

    def load_blocks(self):
        for file_path in self.get_file_paths(SPIMI_INDEX_BLOCKS_PATH):
            self.blocks.append(csv.reader(open(file_path, newline='')))

    def merge_blocks(self):
        merge_completed = False
        spimi_index_writer = csv.writer(open(SPIMI_INDEX_PATH, 'w'))
        temp_index = {}

        # initial index load
        for block_idx, block in enumerate(self.blocks):
            term, postings_list = next(self.blocks[block_idx])
            temp_index[block_idx] = TermItem(term, set(json.loads(postings_list)))

        # merge blocks from temp_index
        while not merge_completed:
            # find least alphabetical ordered term in all blocks
            min_term = min(temp_index.values(), key=lambda x: x.term)
            min_blocks_idxes = [
                block_idx
                for block_idx, term_item in temp_index.items()
                if term_item.term == min_term.term
            ]
            min_term_items = [
                item.postings_list
                for idx, item in temp_index.items()
                if idx in min_blocks_idxes
            ]
            min_postings_list = list(reduce(lambda x, y: x | y, min_term_items))

            # write to final index
            spimi_index_writer.writerow(
                [min_term.term, json.dumps(min_postings_list)]
            )

            # Collect the next entries from blocks
            for block_id in min_blocks_idxes:
                term_item = next(self.blocks[block_id], None)
                if term_item:
                    term, postings_list = term_item
                    temp_index[block_id] = \
                        TermItem(term, set(json.loads(postings_list)))

                # remove empty blocks from temp index
                else:
                    del temp_index[block_id]

            if not temp_index:
                merge_completed = True

    @classmethod
    def _get_sorted_index_terms_list(cls, index):
        return sorted(index.items())

    @classmethod
    def _save_block(cls, block_idx, terms_index_list):
        dir_path = SPIMI_INDEX_BLOCKS_PATH
        block_name = 'block-{}.csv'.format(block_idx)
        block_path = dir_path + block_name

        with open(block_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for k, v in terms_index_list:
                writer.writerow([k, json.dumps(list(map(lambda x: x.doc, v)))])


SPIMIIndexBuilder().run(INPUT_DIR_PATH)
