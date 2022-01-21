"""
Output manager / Compiled data handler.
"""
from typing import List, Set

from src.pybuiltins.PyPortFunction import PyPortFunction
from src.pyexpressions.PyExpression import PyExpression


class Output:
	"""
	Output handler (saves output and expression nodes).
	"""

	__output: List[PyExpression]

	def __init__(self) -> None:
		# Initialize output segment
		self.__output = []

	def write(self, expression: PyExpression) -> None:
		"""
		Append the expression to the output.

		@param expression: The expression to append.
		"""
		self.__output.append(expression)

	def get_output_as_list(self) -> List[str]:
		"""
		Returns the compiled output as a list of strings.
		"""
		# Make lists
		output_list: List[str] = []
		depends_list: Set[str] = set()
		native_depends_list: Set[PyPortFunction] = set()

		# For each section of the code
		for expression in self.__output:
			# Add dependencies to the output
			depends_list.update(expression.get_dependencies())
			# Add native dependencies to the output
			native_depends_list.update(expression.get_native_dependencies())
			# Transpile each segment and add it to the output
			output_list.append(expression.__transpile())

		# Inject dependencies
		# This runs in exponential time (.insert is linear, external 'for' loop is linear)
		# If optimizations are required later, check out "collections.deque".

		# For each native dependency
		for native_dependency in native_depends_list:
			# Insert dependency
			output_list.insert(0, native_dependency.transpile())

		# For each dependency
		for dependency in depends_list:
			# Insert dependency
			output_list.insert(0, f"#include <{dependency}>")

		# Return the output
		return output_list

	def get_output(self) -> str:
		"""
		Returns the compiled output as a string.
		"""
		return "\n".join(self.get_output_as_list())
