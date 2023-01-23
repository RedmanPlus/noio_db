from importlib import import_module
from typing import Union

from noio_db.core import AST, SelectSQLQueryConstructor
from noio_db.settings import Settings
from noio_db.utils import zip_into_dict


class Query:

    query_constructor = SelectSQLQueryConstructor()

    def __init__(self, model, ast: AST):

        self.model_class = model
        self.objects: list = []
        self.called = False
        self.query_ast: Union[AST, None] = ast

        self.is_called_async: bool = False

        if user_settings := Settings.__subclasses__():
            self.db_driver = import_module(user_settings[0]().driver_path).Driver(
                self, user_settings[0]()
            )
        else:
            self.db_driver = import_module(Settings().driver_path).Driver(
                self, Settings()
            )

    def __getitem__(self, item):

        if not self.called:
            query = self.query_constructor.compile(self.query_ast.to_dict())
            self.objects = self.db_driver(query)

            model_annotations = self.model_class.__annotations__
            model_field_names = list(model_annotations.keys())
            model_field_names.insert(0, "id")

            for i, result in enumerate(self.objects):
                kwargs = zip_into_dict(model_field_names, result)
                self.objects[i] = self.model_class(**kwargs)

            self.called = True
        return self.objects[item]
