from noio_db.core.sql_object_factories import AbstractSQLObjectFactory
from noio_db.core.sql_objects import BaseSQLObject, DeleteSQLObject


class DeleteSQLObjectFactory(AbstractSQLObjectFactory):
    def get_object(self, *args) -> BaseSQLObject:

        table = args[0]

        if len(args) > 1:
            raise Exception("Delete SQL object gets only source table name")

        return DeleteSQLObject(table)
