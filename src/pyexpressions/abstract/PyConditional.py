"""
PyConditional base class.
Extends other conditional expressions such as if, if/else, while...
"""
from _ast import AST
from typing import Union, Optional, List

from src.compiler.Compiler import Compiler
from src.pybuiltins.PyPortFunction import PyPortFunction
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyCompare import PyCompare
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyConditional(PyExpression):
	"""
	PyConditional base class.
	"""

	__prefix: str
	__code: List[PyExpression]
	__condition: PyCompare

	def __init__(self, expression: Union[AST, "PyPortFunction"], prefix: str, parent: Optional[GENERIC_PYEXPR_TYPE]):
		super().__init__(expression, parent)
		# Set prefix to our prefix
		self.__prefix = prefix
		# Copy each PyExpression to the body
		self.__code = [self.from_ast(ast) for ast in expression.body]
		# Get condition
		self.__condition = PyCompare(Compiler.get_attr(expression, 'test'), self)

	def _transpile(self) -> str:
		"""
		Transpiles this expression to a C++ string.

		This is the *wrapped* method. We (the devs) will use this method
		to *IMPLEMENT* the transpilation process. To actually transpile
		the code, use the self.transpile method, which wraps this method.
		"""
		return f"{self.__prefix} ({self.__condition.transpile()}) {{{''.join([expr.transpile() for expr in self.__code])}}}"
