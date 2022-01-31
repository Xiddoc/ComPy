"""
Function argument name declaration.
"""
from _ast import arg

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
		from src.compiler.Compiler import Compiler
		self.__arg_type = PyName(Compiler.get_attr(expression, 'annotation'), self)

	def _transpile(self) -> str:
		"""
		Transpiles the constant to a string.
		"""
		return f"{self.__arg_type.transpile()} {self.__arg_name}"