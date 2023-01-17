from abc import ABC, abstractmethod
from core.sql_objects import (BaseSQLObject,
                         SelectSQLObject,
                         FromSQLObject,
                         WhereSQLObject,
                         JoinSQLObject,
                         AndSQLObject,
                         OrSQLObject,
                         ArgInBracesSQLObject,
                         AsSQLObject)


class AbstractSQLObjectFactory(ABC):

    @abstractmethod
    def get_object(self, *args) -> BaseSQLObject:
        pass

    #@abstractmethod
    #async def get_object_async(self, *args) -> BaseSQLObject:
    #    pass


class SelectSQLObjectFactory(AbstractSQLObjectFactory):

    def get_object(self, *args) -> BaseSQLObject:
        args = ", ".join(args)
        return SelectSQLObject(args)


class PairOPSQLObjectFactory(AbstractSQLObjectFactory):

    object_class: BaseSQLObject

    def get_object(self, *args) -> BaseSQLObject:
        if len(args) >= 2:
            args = [args[i:i+2] for i in range(0, len(args), 2)]
        pairs = []
        for arg_pair in args:
            if len(arg_pair) < 2:
                pairs.append(arg_pair[0])
                continue
            pairs.append(self.object_class(*arg_pair))
        while len(pairs) > 1:
            pairs[0] = self.object_class(pairs[0], pairs[1])
            pairs.pop(1)

        return pairs[0]


class AndSQLObjectFactory(PairOPSQLObjectFactory):

    object_class = AndSQLObject


class OrSQLObjectFactory(PairOPSQLObjectFactory):

    object_class = OrSQLObject


class AsSQLObjectFactory(PairOPSQLObjectFactory):

    object_class = AsSQLObject


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
                        conditions[i+j] = f"{field_a}={field_b}"
            join = JoinSQLObjectFactory() \
                .get_object(
                    *args[:-1],
                    "FULL OUTER",
                    *list(conditions.values())
                )

            return FromSQLObject(join)

        return FromSQLObject(*args)


class WhereSQLObjectFactory(AbstractSQLObjectFactory):

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

        return ArgInBracesSQLObject(
            query_type.get_object(
                query_args
            )
        )

    def get_object(self, *args) -> BaseSQLObject:

        query = args[0]

        if isinstance(query, str):

            return WhereSQLObject(query)

        if len(query) > 1:

            raise Exception(
                "Number of high level agruments must be one to determine "
                "top separator"
            )

        if not self.key_clauses.get(list(query.keys())[0]):

            raise Exception(
                "Unknown clause"
            )

        compiled_args = self._get_subqueries(query)

        return WhereSQLObject(compiled_args)
