"""
Assign a value to a variable.
"""
from _ast import Assign

from src.compiler.Compiler import Compiler
from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyAssign(PyExpression):
	"""
	Expression for assigning a variable.
	"""

	__target: str
	__value: PyExpression

	def __init__(self, expression: Assign, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Get the target variable(s) (could be Tuple of variables, but we don't support that currently)
		# Get the first variable, then get the stored ID
		self.__target = Util.get_attr(Util.get_attr(expression, "targets")[0], "id")
		# Get the set value, convert it and store
		self.__value = self.from_ast(Util.get_attr(expression, "value"))

	def _transpile(self) -> str:
		"""
		Transpile the operation to a string.
		"""
		return f"{self.__target} = {self.__value.transpile()};"
