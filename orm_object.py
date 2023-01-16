from pydantic import BaseModel
from sql_query_constructors import SelectSQLQueryConstructor


class SelectMixin:


    @classmethod
    def _get_fields(cls) -> dict:
        return cls.__annotations__

    @classmethod
    def _get_sync(cls, **kwargs) -> str:
        fields = cls._get_fields()
        for k, v in kwargs.items():
            field_val = fields.get(k, False)

            if not field_val:

                raise Exception(
                    f"Unknown attribute: {k}"
                )

            query = {
                "select": ["*"],
                "from": [cls.__name__.lower()],
                "where": {
                    "and": [f"{k}={v}" for k, v in kwargs.items()],
                },
            }

        return SelectSQLQueryConstructor().compile(query)

    @classmethod
    async def _get_async(cls, **kwargs) -> str:

        return cls._get_sync(**kwargs)


    @classmethod
    def get(cls, **kwargs) -> str:


class Demo(BaseModel, SelectMixin):

    a: int
    b: int


print(Demo.get(a=5, b=6))
