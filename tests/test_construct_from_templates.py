import pytest


# pylint: disable=W0613
class TestTemplates:
    @pytest.mark.filterwarnings
    def test_simple_query(self, query, snapshot):
        snapshot.assert_match()


# pylint: enable=W0613
