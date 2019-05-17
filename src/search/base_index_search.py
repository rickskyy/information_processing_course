class Operator:

    AND = '&&'
    OR = '||'

    @staticmethod
    def operators():
        return [Operator.AND, Operator.OR]


class BaseIndexSearch:

    def search(self, query_str):
        pass

    @staticmethod
    def _apply_operator(token1, token2, operator):
        token1, token2 = set(token1), set(token2)
        if operator == Operator.AND:
            return list(token1.intersection(token2))
        elif operator == Operator.OR:
            return list(token1.union(token2))
        else:
            raise Exception()

    @staticmethod
    def _prepare_query_str(query_str):
        _list = filter(None, map(lambda x: x.strip(), query_str.split(' ')))
        _list = map(lambda x: '&&' if x == 'AND' else x, _list)
        _list = map(lambda x: '||' if x == 'OR' else x, _list)
        _list = map(lambda x: x.lower(), _list)
        return list(_list)
