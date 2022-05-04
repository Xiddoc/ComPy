"""
Function argument name declaration.
"""
from _ast import arg, Name
from typing import Optional, cast

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyName import PyName
from src.pyexpressions.highlevel.PyIdentifiable import PyIdentifiable
from src.structures.Errors import SyntaxSubsetError
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyArg(PyIdentifiable):
    """
    Function argument name declaration.
    """

    __arg_type: PyName
    __self_arg: bool

    def __init__(self, expression: arg, parent: GENERIC_PYEXPR_TYPE):
        super().__init__(expression, parent)

        # Convert and store
        self.set_id(expression.arg)

        # Arg type annotation
        type_hint: Optional[Name] = Util.get_attr(expression, 'annotation')

        # If the argument is 'self' (constructor parameter)
        if self.get_id() == "self":
            # Get the name of the class we are referring to
            class_name: str
            try:
                from src.pyexpressions.concrete.PyClassDef import PyClassDef
                # Get the class name
                # Case to PyExpression (our parent is a function)
                # Cast to PyClassDef, then get the class name
                # This might throw an error (hence the 'except' catch),
                # but it follows the Python concept of "Try, and ask of forgiveness".
                class_name = cast(PyClassDef, cast(PyExpression, self.get_parent()).get_parent()).get_id()
            except AttributeError:
                raise SyntaxSubsetError("missing type")

            # Convert to PyName expression
            self.__arg_type = PyName(Name(class_name, None), self)
            self.__self_arg = True
        # If it has a type, then it must be an argument
        elif type_hint is not None:
            # Then it's a normal argument
            self.__arg_type = PyName(type_hint, self)
            self.__self_arg = False
        else:
            raise SyntaxSubsetError("missing type")

    def is_self_arg(self) -> bool:
        """
        :return: Returns True if this argument is the instance self-reference.
        """
        return self.__self_arg

    def get_type(self) -> PyName:
        """
        :return: The type of the function argument, as a PyName instance.
        """
        return self.__arg_type

    def _transpile(self) -> str:
        """
        Transpiles the constant to a string.
        """
        return f"{self.__arg_type.transpile()} {self.get_id()}"
