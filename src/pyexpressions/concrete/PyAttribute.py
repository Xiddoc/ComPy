"""
Attribute statement (object inside another object, usually classes).
"""
from _ast import Attribute

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyName import PyName
from src.pyexpressions.highlevel.PyIdentifiable import PyIdentifiable
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyAttribute(PyExpression, PyIdentifiable):
    """
	Attribute statement (object inside another object, usually classes).
	"""

    __parent_object: PyName

    def __init__(self, expression: Attribute, parent: GENERIC_PYEXPR_TYPE):
        super().__init__(expression, parent)

        # Get the attribute name
        self.set_id(expression.attr)

        # Set the attribute's parent-object
        # Value might reveal a method later in the future
        self.__parent_object = PyName(Util.get_attr(expression, "value"), self)

    def _transpile(self) -> str:
        """
		Transpiles the constant to a string.
		"""
        return f"{self.__parent_object.transpile()}.{self.get_id()}"
