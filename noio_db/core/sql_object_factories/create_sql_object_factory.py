from noio_db.core.sql_object_factories import AbstractSQLObjectFactory
from noio_db.core.sql_objects import (
    ArgInBracesSQLObject,
    BaseSQLObject,
    CommaSQLObject,
    CreateTableArgSQLObject,
    CreateTableSQLObject,
)
from noio_db.utils import SQLITE_MAPPINGS


class CreateTableSQLObjectFactory(AbstractSQLObjectFactory):
    def get_object(self, *args) -> BaseSQLObject:

        if len(args) == 1:
            raise Exception(
                f"Cannot create table {args[0]} - no fields for the database provided"
            )

        name = args[0]
        table_args = []
        for k, v in args[1].items():

            if _map := SQLITE_MAPPINGS.get(v, False):
                table_arg = CreateTableArgSQLObject(k, _map)
                table_args.append(table_arg)
                continue

            raise Exception(f"Cannot map type {v} to any known SQL mappings")

        res_arg = None
        for i, arg in enumerate(table_args):
            if i == 0:
                res_arg = CommaSQLObject(arg, table_args[i + 1])
                continue

            if i == len(table_args) - 1:
                break

            res_arg = CommaSQLObject(res_arg, table_args[i + 1])

        return CreateTableSQLObject(name, ArgInBracesSQLObject(res_arg))
