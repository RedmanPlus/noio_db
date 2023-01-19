from abc import ABC, abstractmethod

from core.sql_objects import BaseSQLObject


class AbstractSQLObjectFactory(ABC):
    @abstractmethod
    def get_object(self, *args) -> BaseSQLObject:
        pass
