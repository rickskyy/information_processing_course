from src.builders.inverse_index_builder import InverseIndexBuilder
from src.constants import INPUT_DIR_PATH
from src.search.base_index_search import BaseIndexSearch, Operator


class InvalidQueryException(Exception):
    pass


class IndexSearch(BaseIndexSearch):

    def __init__(self):
        self.index_builder = InverseIndexBuilder()
        self.index = self.index_builder.build_index(INPUT_DIR_PATH)

    def search(self, query_str):
        query_words = self._prepare_query_str(query_str)
        if not query_words:
            return []
        elif query_words[0] in Operator.operators():
            raise InvalidQueryException()

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
        return postfix_tokens

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
            return list(map(lambda x: x.doc, self.index[token]))


s = IndexSearch()
print(s.search('light AND be AND Day AND firmament'))
print(s.search('light AND be OR Day'))
