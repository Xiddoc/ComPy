"""
Attribute statement (object inside another object, usually classes).
"""
from _ast import Attribute

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.highlevel.PyIdentifiable import PyIdentifiable
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyAttribute(PyIdentifiable):
    """
    Attribute statement (object inside another object, usually classes).
    """

    __parent_object: PyIdentifiable

    def __init__(self, expression: Attribute, parent: GENERIC_PYEXPR_TYPE):
        super().__init__(expression, parent)

        # Get the attribute name
        self.set_id(expression.attr)

        # Set the attribute's parent object
        self.__parent_object = self.from_ast(Util.get_attr(expression, "value"))

    def _transpile(self) -> str:
        """
        Transpiles the constant to a string.
        """
        # If the parent is "self", then we are referencing a class field
        if self.__parent_object.get_id() == "self":
            # In C++ we don't use "self", we just reference the name directly
            return self.get_id()
        else:
            # Otherwise, add the attribute parent
            return f"{self.__parent_object.transpile()}.{self.get_id()}"
