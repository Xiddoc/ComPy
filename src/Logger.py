"""
Logging utilities and functions.
"""
from src.pyexpressions.PyExpression import PyExpression


class Logger:
	"""
	Logger class.

	Lightweight instance that belongs to and
	is passed between to each classes.
	"""

	__indentation: int

	def __init__(self, py_expr: PyExpression) -> None:
		# Figure out indentation level
		# We do this by figuring out how many parents there are to this node.
		temp_expr: PyExpression = py_expr
		indentation: int = 0

		# Keep iterating down the "parent node chain"
		while temp_expr.get_parent() is not None:
			# Increment the count
			indentation += 1
			# Iterate to next parent
			temp_expr = temp_expr.get_parent()

		# Set to field
		self.__indentation = indentation

	def log(self, message: str) -> None:
		"""
		Logs a string to standard output.
		Automatically formats the string.

		@param message: The message to log.
		"""
		print("\t" * self.__indentation + message)
