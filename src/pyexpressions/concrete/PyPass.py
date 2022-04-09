"""
Pass statement.
"""
from _ast import Pass

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyPass(PyExpression):
    """
    Pass statement.
    """

    def __init__(self, expression: Pass, parent: GENERIC_PYEXPR_TYPE):
        super().__init__(expression, parent)

    def _transpile(self) -> str:
        """
        Transpiles the constant to a string.
        """
        return ""
