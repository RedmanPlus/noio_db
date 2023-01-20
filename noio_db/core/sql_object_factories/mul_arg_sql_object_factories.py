from noio_db.core.sql_objects import (
    BaseSQLObject,
    CommaSQLObject,
    GroupBySQLObject,
    OrderBySQLObject,
    SelectSQLObject,
)

from .abstract_sql_object_factory import AbstractSQLObjectFactory


class MulArgsSQLObjectFactory(AbstractSQLObjectFactory):

    SQLObjectClass: BaseSQLObject

    def get_object(self, *args) -> BaseSQLObject:
        root = args[0]
        if isinstance(root, str):
            return self.SQLObjectClass(root)
        if len(args) > 1:
            root = None
            for i, arg in enumerate(args):
                if i == 0:
                    root = CommaSQLObject(arg, args[i + 1])
                    continue
                if i == len(args) - 1:
                    break

                root = CommaSQLObject(root, args[i + 1])

        return self.SQLObjectClass(root)


class SelectSQLObjectFactory(MulArgsSQLObjectFactory):

    SQLObjectClass = SelectSQLObject


class GroupBySQLObjectFactory(MulArgsSQLObjectFactory):

    SQLObjectClass = GroupBySQLObject


class OrderBySQLObjectFactory(MulArgsSQLObjectFactory):

    SQLObjectClass = OrderBySQLObject
