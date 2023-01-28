from abc import ABC, abstractmethod
from typing import Dict

from noio_db.core.sql_object_factories import (
    AbstractSQLObjectFactory,
    FromSQLObjectFactory,
    GroupBySQLObjectFactory,
    HavingSQLObjectFactory,
    InsertSQLObjectFactory,
    OrderBySQLObjectFactory,
    SelectSQLObjectFactory,
    SetSQLObjectFactory,
    UpdateSQLObjectFactory,
    WhereSQLObjectFactory,
)


class AbstractSQLQueryConstructor(ABC):

    constructor_markers: Dict[str, AbstractSQLObjectFactory]

    @abstractmethod
    def compile(self, query: dict) -> str:
        pass


class SelectSQLQueryConstructor(AbstractSQLQueryConstructor):

    constructor_markers = {
        "select": SelectSQLObjectFactory(),
        "from": FromSQLObjectFactory(),
        "where": WhereSQLObjectFactory(),
        "group_by": GroupBySQLObjectFactory(),
        "having": HavingSQLObjectFactory(),
        "order_by": OrderBySQLObjectFactory(),
        "insert": InsertSQLObjectFactory(),
        "update": UpdateSQLObjectFactory(),
        "set": SetSQLObjectFactory(),
    }

    def compile(self, query: dict) -> str:

        sql_strings = []

        for k, v in query.items():

            if isinstance(v, (dict, str)):
                sql_strings.append(self.constructor_markers.get(k).get_object(v))
                continue

            sql_strings.append(self.constructor_markers.get(k).get_object(*v))

        return " ".join([i.compile() for i in sql_strings]) + ";"
