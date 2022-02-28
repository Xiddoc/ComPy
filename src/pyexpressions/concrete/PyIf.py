"""
Class for a conditional statement.
"""
from _ast import If
from typing import Optional, List

from src.pyexpressions.abstract.PyConditional import PyConditional
from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.highlevel.PyBody import PyBody
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyIf(PyConditional):
	"""
	Class for a Python conditional statement.
	"""

	__else: Optional[PyBody]

	def __init__(self, expression: If, parent: GENERIC_PYEXPR_TYPE, if_type: str = "if"):
		super().__init__(expression, if_type, parent)
		# Defaults
		self.__else = None
		# If there is an "or else"
		orelse_list = expression.orelse
		if orelse_list:
			# Send to "else"
			self.__else = PyBody(orelse_list, self)

	def _transpile(self) -> str:
		"""
		Transpile the conditional statement to a string.
		"""
		return super()._transpile() + (f" else {self.__else.transpile()}" if self.__else else "")
