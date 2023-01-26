from typing import Union

from noio_db.core import AST, SelectSQLQueryConstructor
from noio_db.utils import get_current_settings, zip_into_dict


class Query:

    query_constructor = SelectSQLQueryConstructor()

    def __init__(self, model, ast: AST):

        self.model_class = model
        self.objects: list = []
        self.called = False
        self.query_ast: Union[AST, None] = ast

        self.is_called_async: bool = False

        self.db_driver = get_current_settings(self)

        self.aiter_count = 0

    def _fill_query(self):

        query = self.query_constructor.compile(self.query_ast.to_dict())
        self.objects = self.db_driver(query)

        model_annotations = self.model_class.__annotations__
        model_field_names = list(model_annotations.keys())
        model_field_names.insert(0, "id")

        for i, result in enumerate(self.objects):
            kwargs = zip_into_dict(model_field_names, result)
            self.objects[i] = self.model_class(__from_orm__=True, **kwargs)

        self.called = True

    def __getitem__(self, item):

        if not self.called:
            self._fill_query()

        return self.objects[item]

    def __iter__(self):

        if not self.called:
            self._fill_query()

        return iter(self.objects)

    def __anext__(self):
        result = self.objects[self.aiter_count]
        self.aiter_count += 1
        return result

    def __aiter__(self):

        if not self.called:
            self._fill_query()

        return self
