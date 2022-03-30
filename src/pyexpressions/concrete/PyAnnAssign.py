"""
Assign an annotation (and possibly a value) to a variable.
"""
from _ast import AnnAssign, Name
from typing import Optional

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyName import PyName
from src.structures.Errors import SyntaxSubsetError
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyAnnAssign(PyExpression):
    """
    Expression for assigning a variable.
    """

    __target: str
    __type: PyName
    __value: Optional[PyExpression]

    def __init__(self, expression: AnnAssign, parent: GENERIC_PYEXPR_TYPE):
        super().__init__(expression, parent)

        # Store variable
        self.__target = Util.get_attr(expression, "target.id")

        # Get type hint
        type_hint: Optional[Name] = Util.get_attr(expression, "annotation")
        # Make sure type hint was passed
        if type_hint is not None:
            # Save it
            self.__type = PyName(type_hint, self)
        else:
            # Raise an error if we do not have a type
            raise SyntaxSubsetError("missing type")

        # If a value is also being assigned
        # (Then the value of expression.value will not be None)
        if expression.value:
            # Convert and store
            self.__value = self.from_ast(Util.get_attr(expression, "value"))
        else:
            # Otherwise, leave as None
            self.__value = None

        # Get the nearest scope
        # Add this variable to the scope
        self.get_nearest_scope().declare_variable(self.__target, self.__type.get_target())

    def get_id(self) -> str:
        """
        :return: Returns the name of the target from the expression.
        """
        return self.__target

    def _transpile(self) -> str:
        """
        Transpile the operation to a string.
        """
        return f"{self.__type.transpile()} {self.__target}" + \
               (f" = {self.__value.transpile()}" if self.__value else "")  # Only transpile value if it exists
