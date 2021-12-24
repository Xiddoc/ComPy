"""
Assign (an annotation) to a variable.
"""
from _ast import AnnAssign

from expressions.PyExpression import PyExpression


class PyAnnAssign(PyExpression):
	"""
	Expression for assigning a variable.
	"""

	__target: str
	__type: str

	def __init__(self, expression: AnnAssign):
		super().__init__(expression)
		# Store variable and type
		self.__target = expression.target.id
		self.__type = expression.annotation.id

	def transpile(self) -> str:
		"""
		Transpile the operation to a string.
		@return:
		"""
		return f"{self.__type} {self.__target};"
