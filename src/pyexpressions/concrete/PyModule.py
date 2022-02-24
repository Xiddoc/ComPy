"""
Python module.
"""
from _ast import Module
from typing import List

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyExpr import PyExpr
from src.pyexpressions.concrete.PyFunctionDef import PyFunctionDef
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
		from src.compiler.Constants import OUTPUT_CODE_TEMPLATE

		# For each expression, we will compile them
		# However, we will separate this into "is a function"
		# or "is not", so that we can put all the function
		# definitions at the top of the output code.
		output_list: List[str] = []
		function_list: List[str] = []
		for pyexpr in self.__body:
			# Transpile each segment and add it to the output
			# If the segment is a function definition
			if isinstance(pyexpr, PyFunctionDef):
				# Add it to the function list
				function_list.append(pyexpr.transpile())
			elif not (isinstance(pyexpr, PyExpr) and pyexpr.is_empty_expression()):
				# Otherwise, check that it's not a dead expression
				# (Any expression which is not a PyExpr that is empty)
				# Transpile and add to code segment
				# https://stackoverflow.com/q/9997895/11985743
				output_list.append(pyexpr.transpile() + ";")

		# Format each part of the output,
		# then format each segment into the template string,
		# then return it all as a string.
		return OUTPUT_CODE_TEMPLATE.format(
			# For each dependency, insert the dependency as a string
			dependency_code="\n".join([f"#include <{dependency}>" for dependency in self.get_dependencies()]),

			# Inject native dependencies (transpile each one)
			ported_code="\n".join([
				native_dependency.transpile() for native_dependency in self.get_ported_dependencies()
			]),

			# Flatten the current code
			transpiled_funcs="\n".join(function_list),

			# Join the transpiled code
			transpiled_code="\n".join(output_list)
		)

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
