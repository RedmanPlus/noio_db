from noio_db.core.sql_object_factories import AbstractSQLObjectFactory
from noio_db.core.sql_objects import BaseSQLObject, SetSQLObject, UpdateSQLObject
from noio_db.utils import list_into_comma_sql_object


class UpdateSQLObjectFactory(AbstractSQLObjectFactory):
    def get_object(self, *args) -> BaseSQLObject:

        if len(args) > 1:
            raise Exception(
                f"Update query must accept only 1 parameter, got {len(args)}"
            )

        name = args[0]

        return UpdateSQLObject(name)


class SetSQLObjectFactory(AbstractSQLObjectFactory):
    def get_object(self, *args) -> BaseSQLObject:

        if len(args) < 1:
            raise Exception("Set query must accept at least one parameter, got 0")

        params = list_into_comma_sql_object(*args)

        return SetSQLObject(params)
