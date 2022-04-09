"""
Constant literal.
"""
from _ast import Constant
from typing import Any

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.Errors import UnsupportedFeatureException
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyConstant(PyExpression):
    """
    Literal constant value.
    """

    __value: str

    def __init__(self, expression: Constant, parent: GENERIC_PYEXPR_TYPE):
        super().__init__(expression, parent)
        # Translate the value
        self.__value = self.translate_constant(expression)

    def _transpile(self) -> str:
        """
        Transpiles the constant to a string.
        """
        return self.__value

    @staticmethod
    def translate_constant(constant: Constant) -> str:
        """
        Transpiles a constant to it's string representation.

        :param constant: The Constant object to transpile.
        """
        from src.compiler.Constants import PY_CONSTANT_CONVERSION_FUNC

        # Get the constant's value
        constant_value: Any = constant.value

        # Get the value's type
        type_name: str = Util.get_name(constant_value)

        # If we can convert it
        if type_name in PY_CONSTANT_CONVERSION_FUNC:
            # Then use the conversion table
            return PY_CONSTANT_CONVERSION_FUNC[type_name](constant_value)
        else:
            # We can't use that
            raise UnsupportedFeatureException(type_name)
