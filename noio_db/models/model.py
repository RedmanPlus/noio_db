# pylint: disable=E0611
from inspect import currentframe, getouterframes

from pydantic import BaseModel

from noio_db.core import AST, CreateTableSQLObjectFactory
from noio_db.query import Query


# pylint: enable=E0611


class SelectMixin:

    is_called_async: bool = False

    @classmethod
    def _get_fields(cls) -> dict:
        return cls.__annotations__

    @classmethod
    def _get_sync(cls, **kwargs) -> Query:
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
    async def _get_async(cls, **kwargs) -> Query:

        return cls._get_sync(**kwargs)

    @classmethod
    def _all_sync(cls) -> Query:

        ast = AST()

        # pylint: disable=W0212
        ast._select("*")
        ast._from(cls.__name__.lower())

        query = Query(model=cls, ast=ast)
        # pylint: enable=W0212

        return query

    @classmethod
    async def _all_async(cls) -> Query:

        return cls._all_sync()

    @classmethod
    def all(cls) -> Query:

        curframe = currentframe()
        outframe = getouterframes(curframe, 1)

        cls.is_called_async = False

        if "await" in outframe[1][4][0]:

            cls.is_called_async = True

            return cls._all_async()

        return cls._all_sync()

    @classmethod
    def get(cls, **kwargs) -> Query:

        curframe = currentframe()
        outframe = getouterframes(curframe, 1)

        cls.is_called_async = False

        if "await" in outframe[1][4][0]:
            cls.is_called_async = True

            return cls._get_async(**kwargs)

        return cls._get_sync(**kwargs)


class CreateModelMixin:
    @classmethod
    def create(cls):
        name = cls.__name__.lower()
        annotations = cls.__annotations__

        return CreateTableSQLObjectFactory().get_object(name, annotations)


class Model(BaseModel, SelectMixin, CreateModelMixin):

    id: int
