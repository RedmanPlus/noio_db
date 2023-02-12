import pytest


class TestGetObject:
    # pylint: disable=W0613
    @pytest.mark.e2e
    def test_get_all_from_db(self, model, settings, db, snapshot):

        query = model.all()

        snapshot.assert_match(str(query.to_json()), "get_all")

    @pytest.mark.e2e
    def test_get_filtered_from_db(self, model, settings, db, snapshot):

        query = model.filter(age=25, name="John Doe")

        snapshot.assert_match(str(query.to_json()), "get_filtered")

    @pytest.mark.e2e
    def test_get_more_filtered_from_db(self, model, settings, db, snapshot):

        query = model.filter(age=25)

        snapshot.assert_match(str(query.to_json()), "get_more_filtered")

    # pylint: enable=W0613
