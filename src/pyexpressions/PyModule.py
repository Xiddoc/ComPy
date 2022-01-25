"""
Python module.
"""
from _ast import Module
from typing import List

from src.pyexpressions.PyExpression import PyExpression
from src.scopes.Scope import Scope


class PyModule(PyExpression):
	"""
	Python module.
	"""

	__body: List[PyExpression]
	__scope: Scope

	def __init__(self, expression: Module):
		super().__init__(expression, None)
		# Create empty object scope
		self.__scope = Scope()
		# For each body expression
		# Create a PyExpression from the AST node
		self.__code = [self.from_ast(ast) for ast in expression.body]

	def _transpile(self) -> str:
		"""
		Transpiles the constant to a native string.
		"""
		return f""

	def get_scope(self) -> Scope:
		"""
		Returns the Scope (instance) of this function body.
		"""
		return self.__scope
