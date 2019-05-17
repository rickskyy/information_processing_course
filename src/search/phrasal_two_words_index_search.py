from src.builders.two_words_index_builder import TwoWordsIndexBuilder
from src.search.inverse_index_search import IndexSearch, Operator
from src.constants import INPUT_DIR_PATH


class InvalidQueryException(Exception):
    pass


class PhrasalTwoWordsIndexSearch(IndexSearch):

    def __init__(self):
        super().__init__()
        self.index_builder = TwoWordsIndexBuilder()
        self.index = self.index_builder.build_index(INPUT_DIR_PATH)

    @staticmethod
    def _prepare_query_str(query_str):
        _list = list(
            filter(None, map(lambda x: x.strip().lower(), query_str.split(' '))))
        _new_list = []
        for i in range(len(_list) - 1):
            _new_list.append((_list[i], _list[i+1]))
            _new_list.append(Operator.AND)
        return _new_list[:-1]


# s = PhrasalTwoWordsIndexSearch()
# print(s.search('led forth the people which'))
