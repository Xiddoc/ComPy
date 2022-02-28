"""
Function argument name declaration.
"""
from _ast import arg

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyName import PyName
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyArg(PyExpression):
	"""
	Function argument name declaration.
	"""

	__arg_name: str
	__arg_type: PyName

	def __init__(self, expression: arg, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Convert and store
		self.__arg_name = expression.arg
		self.__arg_type = PyName(Util.get_attr(expression, 'annotation'), self)

	def get_name(self) -> str:
		"""
		:return: The name of the function argument, as a string.
		"""
		return self.__arg_name

	def get_type(self) -> PyName:
		"""
		:return: The type of the function argument, as a PyName instance.
		"""
		return self.__arg_type

	def _transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return f"{self.__arg_type.transpile()} {self.__arg_name}"
