"""
Python module.
"""
from _ast import Module
from typing import List, Set

from src.pybuiltins.PyPortFunction import PyPortFunction
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
		self.__body = [self.from_ast(ast) for ast in expression.body]

	def _transpile(self) -> str:
		"""
		Transpiles the module to a native string.
		"""
		# Make lists
		output_list: List[str] = []
		depends_list: Set[str] = set()
		native_depends_list: Set[PyPortFunction] = set()

		# For each section of the code
		for pyexpr in self.__body:
			# Add dependencies to the output
			depends_list.update(pyexpr.get_dependencies())
			# Add native dependencies to the output
			native_depends_list.update(pyexpr.get_ported_dependencies())
			# Transpile each segment and add it to the output
			output_list.append(pyexpr.transpile())

		# Inject dependencies (Check out "collections.deque" later, if necessary for optimization)

		# For each native dependency
		for native_dependency in native_depends_list:
			# Insert dependency
			output_list.insert(0, native_dependency.transpile())

		# For each dependency
		for dependency in depends_list:
			# Insert dependency
			output_list.insert(0, f"#include <{dependency}>")

		# Return the output as a string
		return "\n".join(output_list)

	def get_scope(self) -> Scope:
		"""
		Returns the Scope (instance) of this function body.
		"""
		return self.__scope
