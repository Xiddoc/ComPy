"""
Python module.
"""
from _ast import Module
from typing import List, Set

from src.pyexpressions.abstract.PyExpression import PyExpression
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
		# Make lists
		output_list: List[str] = []
		function_list: List[str] = []
		depends_list: Set[str] = set()

		# For each expression, we will compile them
		# However, we will separate this into "is a function"
		# or "is not", so that we can put all the function
		# definitions at the top of the output code.
		for pyexpr in self.__body:
			# Transpile each segment and add it to the output
			# If the segment is a function definition
			if isinstance(pyexpr, PyFunctionDef):
				# Add it to the function list
				function_list.append(pyexpr.transpile())
			else:
				# Otherwise, add the code segment to the code section
				output_list.append(pyexpr.transpile())

		# Flatten the current code
		# Start by transpiling the functions
		transpiled_funcs: str = "\n".join(function_list)

		# Join the transpiled code
		transpiled_code: str = "\n".join(output_list)

		# Inject native dependencies (transpile each one)
		native_object_code: str = "\n".join([
			native_dependency.transpile() for native_dependency in self.get_ported_dependencies()
		])

		# Get a unique set of dependencies (imports) to add to the output code
		depends_list.update(self.get_dependencies())

		# For each dependency, insert the dependency as a string
		native_dependency_code: str = "\n".join([f"#include <{dependency}>" for dependency in depends_list])

		# Merge the output, then return as a string
		return f"""
{native_dependency_code}

{native_object_code}

{transpiled_funcs}

int main() {{
	/* Transpiled with ComPy */
	{transpiled_code}
	return 0;
}}"""

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
