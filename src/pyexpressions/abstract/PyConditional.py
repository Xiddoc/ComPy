"""
PyConditional base class.
Extends other conditional expressions such as if, if/else, while...
"""
from _ast import AST
from typing import Optional, List

from src.compiler.Util import Util
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyConditional(PyExpression):
	"""
	PyConditional base class.
	"""

	__prefix: str
	__code: List[PyExpression]
	__condition: PyExpression

	def __init__(self, expression: AST, prefix: str, parent: Optional[GENERIC_PYEXPR_TYPE]):
		super().__init__(expression, parent)
		# Set prefix to our prefix
		self.__prefix = prefix
		# Copy each PyExpression to the body
		self.__code = [self.from_ast(ast) for ast in expression.body]
		# Get condition
		self.__condition = self.from_ast(Util.get_attr(expression, 'test'))

	def _transpile(self) -> str:
		"""
		Transpiles this expression to a C++ string.

		This is the *wrapped* method. We (the devs) will use this method
		to *IMPLEMENT* the transpilation process. To actually transpile
		the code, use the self.transpile method, which wraps this method.
		"""
		return f"{self.__prefix} ({self.__condition.transpile()}) {{{''.join([expr.transpile() for expr in self.__code])}}}"
