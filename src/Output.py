"""
Output manager / Compiled data handler.
"""
from typing import List

from src.expressions.PyExpression import PyExpression


class Output:
	"""
	Output handler (saves output and expression nodes).
	"""

	__output: List[PyExpression]

	def __init__(self):
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
		# Make list
		output_list: List[str] = []
		# For each section of the code
		for expression in self.__output:
			# Transpile each segment
			output_list.append(expression.transpile())
		# Return the output
		return output_list

	def get_output(self) -> str:
		"""
		Returns the compiled output as a string.
		"""
		return "\n".join(self.get_output_as_list())
