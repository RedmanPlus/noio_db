from noio_db.core.sql_objects import (
    BaseSQLObject,
    GroupBySQLObject,
    OrderBySQLObject,
    SelectSQLObject,
)
from noio_db.utils import list_into_comma_sql_object

from .abstract_sql_object_factory import AbstractSQLObjectFactory


class MulArgsSQLObjectFactory(AbstractSQLObjectFactory):

    SQLObjectClass: BaseSQLObject

    def get_object(self, *args) -> BaseSQLObject:
        root = args[0]
        if isinstance(root, str):
            return self.SQLObjectClass(root)
        if len(args) > 1:
            root = list_into_comma_sql_object(*args)

        return self.SQLObjectClass(root)


class SelectSQLObjectFactory(MulArgsSQLObjectFactory):

    SQLObjectClass = SelectSQLObject


class GroupBySQLObjectFactory(MulArgsSQLObjectFactory):

    SQLObjectClass = GroupBySQLObject


class OrderBySQLObjectFactory(MulArgsSQLObjectFactory):

    SQLObjectClass = OrderBySQLObject
