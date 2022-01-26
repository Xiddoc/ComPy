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
			# Add native dependencies of PyPorts
			depends_list.update(native_dependency.get_native_dependencies())

		# For each dependency
		for dependency in depends_list:
			# Insert dependency
			output_list.insert(0, f"#include <{dependency}>")

		# Return the output as a string
		return "\n".join(output_list)

	# noinspection PyUnusedFunction
	def get_scope(self) -> Scope:
		"""
		Returns the Scope (instance) of this module body.

		Might have a warning in your IDE that labels it as "unused".
		This is since it is not explicitly used (in PyExpression:
		it *should* be casted to PyFunctionDef, then use obj.get_scope(),
		but instead there is a type check, then we use get_scope.

		What this means is that depending on the Python linter
		implementation, your IDE could flag this function as useless.
		It is not. Do **NOT** remove it.
		"""
		return self.__scope
