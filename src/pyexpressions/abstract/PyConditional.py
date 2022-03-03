"""
PyConditional base class.
Extends other conditional expressions such as if, if/else, while...
"""
from _ast import AST
from typing import Optional

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.highlevel.PyBody import PyBody
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyConditional(PyExpression):
    """
    PyConditional base class.
    """

    __code: PyExpression
    __condition: PyExpression

    def __init__(self, expression: AST, parent: Optional[GENERIC_PYEXPR_TYPE]):
        super().__init__(expression, parent)
        # Copy each PyExpression to the body
        code_instance = Util.get_attr(expression, 'body')
        self.__code = PyBody(code_instance, self) if isinstance(code_instance, list) else self.from_ast(code_instance)
        # Get condition
        self.__condition = self.from_ast(Util.get_attr(expression, 'test'))

    def _transpile(self) -> str:
        """
        Transpiles this expression to a C++ string.

        This is the *wrapped* method. We (the devs) will use this method
        to *IMPLEMENT* the transpilation process. To actually transpile
        the code, use the self.transpile method, which wraps this method.
        """
        return f"({self.transpile_condition()}) {self.transpile_body()}"

    def transpile_condition(self) -> str:
        """
        :return: The string representation of the conditional's condition.
        """
        return self.__condition.transpile()

    def transpile_body(self) -> str:
        """
        :return: The string representation of the conditional's body.
        """
        return self.__code.transpile()
