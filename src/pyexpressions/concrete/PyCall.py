"""
Call a function.
"""
from _ast import Call
from typing import List

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyCall(PyExpression):
    """
    Call a function.
    """

    __args: List[PyExpression]
    __obj: PyExpression

    def __init__(self, expression: Call, parent: GENERIC_PYEXPR_TYPE):
        super().__init__(expression, parent)
        # Convert to name
        self.__obj = self.from_ast(expression.func)

        # For each argument
        # Convert to argument object and store
        self.__args = [self.from_ast(arg) for arg in expression.args]

    def _transpile(self) -> str:
        """
        Transpile the operation to a string.
        """
        # Transpile the actual function call to the matching native code...
        # Take function name
        # Add parenthesis
        # For each argument, transpile
        # Join the arguments together with commas
        # FUNC_NAME ( ARG1 , ARG2 , ... )
        return f"{self.__obj.transpile()}({','.join([arg.transpile() for arg in self.__args])})"
