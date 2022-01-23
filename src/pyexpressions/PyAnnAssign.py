"""
Assign an annotation (and possibly a value) to a variable.
"""
from _ast import AnnAssign
from typing import Optional

from src.compiler.Compiler import Compiler
from src.pyexpressions.PyExpression import PyExpression
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyAnnAssign(PyExpression):
	"""
	Expression for assigning a variable.
	"""

	__target: str
	__type: str
	__value: Optional[PyExpression]

	def __init__(self, expression: AnnAssign, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Store variable and type
		self.__target = Compiler.get_attr(expression, "target.id")
		self.__type = Compiler.get_attr(expression, "annotation.id")

		# If a value is also being assigned
		# (Then the value of expression.value will not be None)
		if expression.value:
			# Convert and store
			self.__value = self.from_ast(Compiler.get_attr(expression, "value"))
		else:
			# Otherwise, leave as None
			self.__value = None

	def _transpile(self) -> str:
		"""
		Transpile the operation to a string.
		"""
		return \
			f"{self.__type} {self.__target} = {self.__value.transpile()};"\
			if self.__value else \
			f"{self.__type} {self.__target};"
