# pylint: disable=E0611
from pydantic import BaseConfig, BaseModel

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

    # @ToAsync
    def insert(self):

        table_name = self.table_name
        table_fields = list(self.__dict__.keys())
        table_fields.pop(0)
        table_values = list(self.__dict__.values())
        table_values.pop(0)

        # pylint: disable=W0212
        ast = AST()
        ast._insert(table_name, table_fields, table_values)
        # pylint: enable=W0212

        query = SelectSQLQueryConstructor().compile(ast.to_dict())
        driver = get_current_settings(self)

        driver(query)


class UpdateMixin:
    def update(self):
        table_name = self.table_name
        updated_fields = self.__dict__
        id_field = updated_fields.pop("id")

        # pylint: disable=W0212
        ast = AST()
        ast._update(table_name)
        ast._set(**updated_fields)
        ast._where(**{"id": id_field})
        # pylint: enable=W0212

        query = SelectSQLQueryConstructor().compile(ast.to_dict())
        driver = get_current_settings(self)

        driver(query)


class DeleteMixin:
    def delete(self):
        table_name = self.table_name
        object_fields = self.__dict__

        id_field = object_fields.pop("id")

        # pylint: disable=W0212
        ast = AST()
        ast._delete(table_name)
        ast._where(id=id_field)

        # pylint: enable=W0212

        query = SelectSQLQueryConstructor().compile(ast.to_dict())
        driver = get_current_settings(self)

        driver(query)


class Model(
    BaseModel, SelectMixin, CreateModelMixin, InsertMixin, UpdateMixin, DeleteMixin
):

    id: int = None

    class Config(BaseConfig):
        is_from_orm: bool = False

    @property
    def table_name(self):
        return self.__class__.__name__.lower()

    @property
    def table_fields(self):
        return list(self.__annotations__.keys())

    @property
    def is_from_orm(self):
        return self.Config.is_from_orm

    @is_from_orm.setter
    def is_from_orm(self, value: bool):
        if not isinstance(value, bool):
            raise Exception()

        self.Config.is_from_orm = value

    def save(self):

        if self.Config.is_from_orm:
            self.update()
        else:
            self.insert()
