import pytest

from noio_db import AST


# pylint: disable=R0913, W0212
class TestAST:
    @pytest.mark.ast_construction
    def test_construct_simple_ast(
        self, select_args, from_args, and_args, or_args, snapshot
    ):
        ast = AST()
        ast._select(*select_args)
        ast._from(*from_args)
        ast._where()
        ast._where._and(**and_args)
        ast._where._and._or(**or_args)

        snapshot.assert_match(str(ast.to_dict()), "ast.txt")


# pylint: enable=R0913, W0212
