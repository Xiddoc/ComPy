"""
Continue statement.
"""
from _ast import Continue

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyContinue(PyExpression):
    """
    Continue statement.
    """

    def __init__(self, expression: Continue, parent: GENERIC_PYEXPR_TYPE):
        super().__init__(expression, parent)

    def _transpile(self) -> str:
        """
        Transpiles the statement to a string.
        """
        return "continue"
