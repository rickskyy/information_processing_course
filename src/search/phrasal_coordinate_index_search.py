from src.builders.coordinate_index_builder import CoordinateIndexBuilder
from src.index_items import CoordinateIndexItem
from src.search.inverse_index_search import IndexSearch, Operator
from src.constants import INPUT_DIR_PATH


class InvalidQueryException(Exception):
    pass


class PhrasalCoordinateIndexSearch(IndexSearch):

    def __init__(self):
        super().__init__()
        self.index_builder = CoordinateIndexBuilder()
        self.index = self.index_builder.build_index(INPUT_DIR_PATH)

    def search(self, query_str, print_nearby=True):
        query_words = self._prepare_query_str(query_str)
        postfix_tokens = self._create_postfix_query_representation(query_words)

        i = 0
        while i < len(postfix_tokens):
            if postfix_tokens[i] in Operator.operators():
                res = self._apply_operator(
                    postfix_tokens[i - 2],
                    postfix_tokens[i - 1],
                    postfix_tokens[i]
                )
                postfix_tokens = postfix_tokens[3:]
                postfix_tokens = [res] + postfix_tokens
                i = 0
            else:
                i += 1

        if print_nearby:
            for item in postfix_tokens[0]:
                print(self.index_builder.show_nearby(item.doc, item.coordinates))

        return postfix_tokens[0]

    def _create_postfix_query_representation(self, query_words):
        curr_operators = []
        postfix = []
        for word in query_words:
            if word in Operator.operators() and curr_operators:
                raise InvalidQueryException()
            elif word in Operator.operators():
                curr_operators.append(word)
            elif word not in Operator.operators() and curr_operators:
                postfix.extend(
                    [self._get_index_item_by_token(word), curr_operators.pop()])
            else:
                postfix.append(self._get_index_item_by_token(word))
        return postfix

    def _get_index_item_by_token(self, token):
        if not self.index.get(token):
            return []
        else:
            return self.index[token]

    def _apply_operator(self, items_list_1, items_list_2, operator):
        if operator == Operator.AND:
            return self._intersection_items(items_list_1, items_list_2)
        else:
            raise Exception()

    def _intersection_items(self, items_list_1, items_list_2):
        _intersection_items_list = []
        for item1 in items_list_1:
            for item2 in items_list_2:
                if item1.doc == item2.doc:
                    _intersection = self._phrasal_intersection_coordinates(
                        item1.coordinates,
                        item2.coordinates
                    )
                    if not _intersection:
                        continue

                    _intersection_items_list.append(
                        CoordinateIndexItem(
                            item1.doc,
                            1,
                            _intersection
                        )
                    )
        return _intersection_items_list

    @staticmethod
    def _phrasal_intersection_coordinates(coords1, coords2):
        intersection_coords = []
        p1, p2 = 0, 0
        while p1 < len(coords1) and p2 < len(coords2):
            if coords1[p1] + 1 == coords2[p2]:
                intersection_coords.append(coords2[p2])
                p1 += 1
                p2 += 1
            elif (coords1[p1] < coords2[p2] and coords1[-1] + 1 < coords2[p2]) \
                    or (coords1[p1] > coords2[p2] and coords1[p1] >= coords2[-1]):
                return intersection_coords
            elif coords1[p1] <= coords2[p2]:
                p1 += 1
            elif coords1[p1] > coords2[p2]:
                p2 += 1

        return intersection_coords

    @staticmethod
    def _prepare_query_str(query_str):
        _list = list(
            filter(None, map(lambda x: x.strip().lower(), query_str.split(' '))))
        _new_list = []
        for item in _list:
            _new_list.append(item)
            _new_list.append(Operator.AND)
        return _new_list[:-1]


s = PhrasalCoordinateIndexSearch()
print(s.search('led forth the people which'))
print(s.search('created the heaven and the'))
print(s.search('the heaven and'))
