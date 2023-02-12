import pytest

from noio_db import AST, SelectSQLQueryConstructor


# pylint: disable=R0913, W0212
class TestASTToSQL:

    constructor = SelectSQLQueryConstructor()

    @pytest.mark.integration
    def test_from_ast_to_sql(
        self, select_args, from_args, and_args, group_by_args, order_by_args, snapshot
    ):
        ast = AST()
        ast._select(*select_args)
        ast._from(*from_args)
        ast._where()
        ast._where._and(**and_args)
        ast._group_by(*group_by_args)
        ast._order_by(*order_by_args)

        snapshot.assert_match(self.constructor.compile(ast.to_dict()), "ast_to_sql.txt")

    @pytest.mark.integration
    def test_delete_from_ast_to_sql(self, delete_table, and_args, snapshot):
        ast = AST()
        ast._delete(delete_table)
        ast._where()
        ast._where._and(**and_args)

        snapshot.assert_match(
            self.constructor.compile(ast.to_dict()), "delete_ast_to_dict.txt"
        )


# pylint: enable=R0913, W0212
