"""
Boolean operation.
"""
from _ast import BoolOp, boolop
from typing import Union, List, cast

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyCompare import PyCompare
from src.structures.Errors import UnsupportedFeatureException
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyBoolOp(PyExpression):
    """
    Expression for boolean operation.
    (Conditional)
    """

    __conditions: List[Union["PyBoolOp", PyCompare]]
    __op_type: str

    def __init__(self, expression: BoolOp, parent: GENERIC_PYEXPR_TYPE):
        super().__init__(expression, parent)
        # Convert op to string
        self.__op_type = f" {self.bool_op_to_str(expression.op)} "
        # Store conditions
        self.__conditions = [cast(Union[PyBoolOp, PyCompare], self.from_ast(condition))
                             for condition in expression.values]

    def _transpile(self) -> str:
        """
        Transpile the operation to a string.
        """
        return f"({self.__op_type.join([condition.transpile() for condition in self.__conditions])})"

    @staticmethod
    def bool_op_to_str(operator: boolop) -> str:
        """
        Transpiles a boolean operator to a string.

        :param operator: The operator to translate
        :return: The operator as a C++ string.
        """
        # Local import to avoid circular import errors
        from src.compiler.Constants import AST_BOOLOP_TO_STR

        # Get the type
        op_type = type(operator)

        # Check if the operator is supported
        if op_type in AST_BOOLOP_TO_STR:
            # Return the translated operator
            return AST_BOOLOP_TO_STR[op_type]
        # Otherwise
        else:
            raise UnsupportedFeatureException(operator)
