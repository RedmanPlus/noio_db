import pytest


class TestModels:
    @pytest.mark.models
    def test_create_model(self, test, snapshot):
        snapshot.assert_match(str(test.create()), "create_table.txt")

    @pytest.mark.models
    def test_get_query_with_model(self, test, snapshot):
        query = test.get(name="John Doe", age=25)
        snapshot.assert_match(query, "get_table.txt")
