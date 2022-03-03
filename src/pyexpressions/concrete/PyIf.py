"""
Class for a conditional statement.
"""
from _ast import If
from typing import Optional

from src.pyexpressions.abstract.PyConditional import PyConditional
from src.pyexpressions.highlevel.PyBody import PyBody
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyIf(PyConditional):
	"""
	Class for a Python conditional statement.
	"""

	__else: Optional[PyBody]

	def __init__(self, expression: If, parent: GENERIC_PYEXPR_TYPE):
		super().__init__(expression, parent)
		# Defaults
		self.__else = None
		# If there is an "or else" (list of expressions)
		if expression.orelse:
			# Send to "else"
			self.__else = PyBody(expression.orelse, self)

	def _transpile(self) -> str:
		"""
		Transpile the conditional statement to a string.
		"""
		return "if " + super()._transpile() + (f" else {self.__else.transpile()}" if self.__else else "")
