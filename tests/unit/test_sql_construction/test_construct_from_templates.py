import pytest

from noio_db import SelectSQLQueryConstructor


# pylint: disable=W0613
class TestTemplates:

    constructor = SelectSQLQueryConstructor()

    @pytest.mark.sql_construction
    def test_simple_query(self, query, snapshot):

        snapshot.assert_match(self.constructor.compile(query), "simple_query.txt")

    @pytest.mark.sql_construction
    def test_full_select_query(self, full_query, snapshot):

        snapshot.assert_match(self.constructor.compile(full_query), "simple_query.txt")


# pylint: enable=W0613
