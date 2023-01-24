# pylint: disable=E0611
from pydantic import BaseModel

from noio_db.core import AST, CreateTableSQLObjectFactory, SelectSQLQueryConstructor
from noio_db.query import Query
from noio_db.utils import ToAsync, get_current_settings


# pylint: enable=E0611
class ObjectCounter:

    __count__: int = 0


class SelectMixin:

    is_called_async: bool = False

    @classmethod
    def _get_fields(cls) -> dict:
        return cls.__annotations__

    @classmethod
    @ToAsync
    def filter(cls, **kwargs) -> Query:
        fields = cls._get_fields()
        for k in kwargs:
            field_val = fields.get(k, False)

            if not field_val:

                raise Exception(f"Unknown attribute: {k}")

        # pylint: disable=W0212, W0106
        ast = AST()
        ast._select("*")
        ast._from(cls.__name__.lower())
        ast._where()
        ast._where._and(**kwargs)
        # pylint: enable=W0212, W0106

        queryset = Query(model=cls, ast=ast)

        return queryset

    @classmethod
    @ToAsync
    def all(cls) -> Query:

        ast = AST()

        # pylint: disable=W0212
        ast._select("*")
        ast._from(cls.__name__.lower())

        query = Query(model=cls, ast=ast)
        # pylint: enable=W0212

        return query


class CreateModelMixin:
    @classmethod
    def create(cls):
        name = cls.__name__.lower()
        annotations = cls.__annotations__

        return CreateTableSQLObjectFactory().get_object(name, annotations)


class InsertMixin:
    def __init__(self, *args, **kwargs):
        self.is_called_async: bool = False
        super().__init__(*args, **kwargs)

    @ToAsync
    def insert(self):

        table_name = self.table_name
        table_fields = list(self.__dict__.keys())
        table_fields.insert(0, "id")
        table_values = list(self.__dict__.values())
        table_values.insert(0, self.__count__)

        # pylint: disable=W0212
        ast = AST()
        ast._insert(table_name, table_fields, table_values)
        # pylint: enable=W0212

        query = SelectSQLQueryConstructor().compile(ast.to_dict())
        driver = get_current_settings(self)

        driver(query)


class Model(BaseModel, SelectMixin, CreateModelMixin, InsertMixin, ObjectCounter):

    __from_orm__: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__count__ += 1

    @property
    def table_name(self):
        return self.__class__.__name__.lower()

    @property
    def table_fields(self):
        return list(self.__annotations__.keys())

    def save(self):
        if self.__from_orm__:
            pass
        else:
            self.insert()
