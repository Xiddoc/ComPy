"""
Assign (an annotation) to a variable.
"""
from _ast import AnnAssign
from typing import Union

from expressions.PyExpression import PyExpression


class PyAnnAssign(PyExpression):
	"""
	Expression for assigning a variable.
	"""

	__target: str
	__type: str
	__value: Union[PyExpression, None]

	def __init__(self, expression: AnnAssign):
		super().__init__(expression)
		# Store variable and type
		self.__target = expression.target.id
		self.__type = expression.annotation.id
		# If a value is also being assigned
		# (Then the value of expression.value will not be None)
		if expression.value:
			# Convert and store
			self.__value = PyExpression.from_ast(expression.value)
		else:
			# Otherwise, leave as None
			self.__value = None

	def transpile(self) -> str:
		"""
		Transpile the operation to a string.
		@return:
		"""
		return \
			f"{self.__type} {self.__target} = {self.__value.transpile()};"\
			if self.__value else \
			f"{self.__type} {self.__target};"
