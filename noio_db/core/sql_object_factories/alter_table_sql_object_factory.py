from noio_db.core.sql_object_factories import AbstractSQLObjectFactory
from noio_db.core.sql_objects import (
    AddSQLObject,
    AlterColumnSQLObject,
    AlterTableSQLObject,
    BaseSQLObject,
    CreateTableArgSQLObject,
    DropSQLObject,
    RenameColumnSQLObject,
)
from noio_db.utils import SQLITE_MAPPINGS, OneArgMixin


class AlterTableSQLObjectFactory(OneArgMixin, AbstractSQLObjectFactory):
    def get_object(self, *args) -> BaseSQLObject:

        table_name = super().get_object(*args)

        return AlterTableSQLObject(table_name)


class ColumnTypeSQLObjectFactory(OneArgMixin, AbstractSQLObjectFactory):

    SQLObject: BaseSQLObject

    def get_object(self, *args) -> BaseSQLObject:

        field = super().get_object(*args)

        k, v = list(field.items())[0]

        if _map := SQLITE_MAPPINGS.get(v, False):

            return k, _map

        raise Exception(f"Cannot map type {v} to any known SQL mappings")


class AlterColumnSQLObjectFactory(ColumnTypeSQLObjectFactory):

    SQLObject = AlterColumnSQLObject

    def get_object(self, *args) -> BaseSQLObject:
        k, _map = super().get_object(*args)

        return AlterColumnSQLObject(k, _map)


class AddSQLObjectFactory(ColumnTypeSQLObjectFactory):

    SQLObject = AddSQLObject

    def get_object(self, *args) -> BaseSQLObject:
        k, _map = super().get_object(*args)

        arg_str = CreateTableArgSQLObject(k, _map)

        return AddSQLObject(arg_str)


class RenameColumnSQLObjectFactory(OneArgMixin, AbstractSQLObjectFactory):
    def get_object(self, *args) -> BaseSQLObject:

        field = super().get_object(*args)

        k, v = list(field.items())[0]

        return RenameColumnSQLObject(k, v)


class DropSQLObjectFactory(OneArgMixin, AbstractSQLObjectFactory):
    def get_object(self, *args) -> BaseSQLObject:

        field = super().get_object(*args)

        return DropSQLObject(field)
