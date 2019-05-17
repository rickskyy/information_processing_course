class BaseIndexItem:
    def __init__(self, doc):
        self.doc = doc


class InverseIndexItem(BaseIndexItem):
    def __init__(self, doc, count, **kwargs):
        super().__init__(doc)
        self.count = count or 0

    def __str__(self):
        return '{} ({})'.format(self.doc, str(self.count))

    def __repr__(self):
        return self.__str__()


class TwoWordsIndexItem(InverseIndexItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CoordinateIndexItem(InverseIndexItem):
    def __init__(self,  doc, count, coordinates, **kwargs):
        super().__init__(doc, count, **kwargs)
        self.coordinates = coordinates or []

    def __str__(self):
        return '{} ({}) ({})'.format(
            self.doc, str(self.count), ', '.join(map(str, self.coordinates))
        )
