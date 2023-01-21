from abc import ABC, abstractmethod

from noio_db.core.sql_objects import BaseSQLObject


class AbstractSQLObjectFactory(ABC):
    @abstractmethod
    def get_object(self, *args) -> BaseSQLObject:
        pass
