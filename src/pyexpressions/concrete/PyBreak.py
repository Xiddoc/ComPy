"""
Break statement.
"""
from _ast import Break

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyBreak(PyExpression):
    """
    Break statement.
    """

    def __init__(self, expression: Break, parent: GENERIC_PYEXPR_TYPE) -> None:
        super().__init__(expression, parent)

    def _transpile(self) -> str:
        """
        Transpiles the statement to a string.
        """
        return "break"
