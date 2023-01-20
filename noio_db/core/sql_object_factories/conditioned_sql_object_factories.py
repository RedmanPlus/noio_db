from noio_db.core.sql_objects import (
    ArgInBracesSQLObject,
    BaseSQLObject,
    HavingSQLObject,
    WhereSQLObject,
)

from .abstract_sql_object_factory import AbstractSQLObjectFactory
from .pair_op_sql_object_factories import AndSQLObjectFactory, OrSQLObjectFactory


class ConditionedSQLObjectFactory(AbstractSQLObjectFactory):

    SQLObjectClass: BaseSQLObject
    key_clauses = {
        "and": AndSQLObjectFactory(),
        "or": OrSQLObjectFactory(),
    }

    def _get_subqueries(self, query: dict) -> BaseSQLObject:

        query_type = self.key_clauses.get(list(query.keys())[0])

        query_args = []
        for item in list(query.values())[0]:
            if isinstance(item, dict):
                item = self._get_subqueries(item)

            query_args.append(item)

        return ArgInBracesSQLObject(query_type.get_object(*query_args))

    def get_object(self, *args) -> BaseSQLObject:

        query = args[0]

        if isinstance(query, str):

            return self.SQLObjectClass(query)

        if len(query) > 1:

            raise Exception(
                "Number of high level agruments must be one to determine "
                "top separator"
            )

        if not self.key_clauses.get(list(query.keys())[0]):

            raise Exception("Unknown clause")

        compiled_args = self._get_subqueries(query)

        return self.SQLObjectClass(compiled_args)


class WhereSQLObjectFactory(ConditionedSQLObjectFactory):

    SQLObjectClass = WhereSQLObject


class HavingSQLObjectFactory(ConditionedSQLObjectFactory):

    SQLObjectClass = HavingSQLObject
