"""
Python "block", conjoined statements.
"""
from _ast import Pass, AST
from typing import List, Sequence

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyExpr import PyExpr
from src.pyexpressions.concrete.PyPass import PyPass
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyBody(PyExpression):
	"""
	Python "block", conjoined statements.
	Such as in a function or conditional body.
	"""

	__code: List[PyExpression]

	def __init__(self, expressions: Sequence[AST], parent: GENERIC_PYEXPR_TYPE):
		super().__init__(Pass(), parent)
		# For each line of code, convert to expression
		# Set expressions to field
		self.__code = [self.from_ast(ast) for ast in expressions]

	def _transpile(self) -> str:
		"""
		Transpile the body to a string.
		"""
		# Join the body together with newlines
		return "{\n" + '\n'.join([
			# Transpile each line
			expr.transpile() + ";" for expr in self.__code \
			# Don't transpile if:
			# - This is a PyExpr which is an empty expression
			# - This is a PyPass expression
			if not (isinstance(expr, PyExpr) and expr.is_empty_expression() or isinstance(expr, PyPass))
		]) + "\n}"
