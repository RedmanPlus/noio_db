# pylint: disable=E0611
from inspect import currentframe, getouterframes

from pydantic import BaseModel

from noio_db.core import AST, CreateTableSQLObjectFactory, SelectSQLQueryConstructor


# pylint: enable=E0611


class SelectMixin:
    @classmethod
    def _get_fields(cls) -> dict:
        return cls.__annotations__

    @classmethod
    def _get_sync(cls, **kwargs) -> str:
        fields = cls._get_fields()
        for k in kwargs:
            field_val = fields.get(k, False)

            if not field_val:

                raise Exception(f"Unknown attribute: {k}")

        # pylint: disable=W0212, W0106
        ast = AST()
        ast._select("*")
        ast._from(cls.__name__.lower()),
        ast._where()
        ast._where._and(**kwargs)
        # pylint: enable=W0212, W0106

        query = ast.to_dict()

        return SelectSQLQueryConstructor().compile(query)

    @classmethod
    async def _get_async(cls, **kwargs) -> str:

        return cls._get_sync(**kwargs)

    @classmethod
    def get(cls, **kwargs) -> str:

        curframe = currentframe()
        outframe = getouterframes(curframe, 1)

        if "await" in outframe[1][4][0]:

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
