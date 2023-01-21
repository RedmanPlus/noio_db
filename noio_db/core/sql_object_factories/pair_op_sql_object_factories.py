from noio_db.core.sql_objects import (
    AndSQLObject,
    AsSQLObject,
    BaseSQLObject,
    OrSQLObject,
)
from noio_db.utils import pair_up_args

from .abstract_sql_object_factory import AbstractSQLObjectFactory


class PairOPSQLObjectFactory(AbstractSQLObjectFactory):

    SQLObjectClass: BaseSQLObject

    def get_object(self, *args) -> BaseSQLObject:
        new_args = list(args)
        if len(args) >= 2:
            new_args = pair_up_args(*args)
        pairs = []
        for arg_pair in new_args:
            if len(arg_pair) < 2:
                pairs.append(arg_pair[0])
                continue
            pairs.append(self.SQLObjectClass(*arg_pair))
        while len(pairs) > 1:
            pairs[0] = self.SQLObjectClass(pairs[0], pairs[1])
            pairs.pop(1)

        return pairs[0]


class AndSQLObjectFactory(PairOPSQLObjectFactory):

    SQLObjectClass = AndSQLObject


class OrSQLObjectFactory(PairOPSQLObjectFactory):

    SQLObjectClass = OrSQLObject


class AsSQLObjectFactory(PairOPSQLObjectFactory):

    SQLObjectClass = AsSQLObject
