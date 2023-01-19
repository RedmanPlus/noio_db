from core.sql_objects import BaseSQLObject, FromSQLObject, JoinSQLObject

from .abstract_sql_object_factory import AbstractSQLObjectFactory
from .pair_op_sql_object_factories import AndSQLObjectFactory


class JoinSQLObjectFactory(AbstractSQLObjectFactory):
    def get_object(self, *args) -> BaseSQLObject:
        join_params = args[3]
        if len(args) > 4:
            join_params = AndSQLObjectFactory().get_object(args[3:])

        return JoinSQLObject(*args[:3], join_params)


class FromSQLObjectFactory(AbstractSQLObjectFactory):
    def get_object(self, *args) -> BaseSQLObject:

        if len(args) == 2:

            raise Exception(
                "Must provide join field if using FROM with multiple tables"
            )

        if len(args) > 2:

            join_field = args[-1]
            fields = []
            for table in args[:-1]:
                fields.append(f"{table}.{join_field}")
            conditions = {}
            for i, field_a in enumerate(fields):
                for j, field_b in enumerate(fields):
                    if i == j:
                        continue
                    if not conditions.get(i + j):
                        conditions[i + j] = f"{field_a}={field_b}"
            join = JoinSQLObjectFactory().get_object(
                *args[:-1], "FULL OUTER", *list(conditions.values())
            )

            return FromSQLObject(join)

        return FromSQLObject(*args)
