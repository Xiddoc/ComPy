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

	def __init__(self, py_expr: "PyExpression") -> None:
		# Figure out indentation level
		# We do this by figuring out how many parents there are to this node.
		temp_expr: "PyExpression" = py_expr
		indentation: int = 0

		# PyPortFunction will throw an error as get_parent does not exist
		try:
			# Keep iterating down the "parent node chain"
			while temp_expr.get_parent() is not None:
				# Increment the count
				indentation += 1
				# Iterate to next parent
				temp_expr = temp_expr.get_parent()
		except AttributeError:
			pass

		# Set to field
		self.__indentation = indentation

	def log(self, message: str) -> None:
		"""
		Logs a string to standard output.
		Automatically formats the string.

		@param message: The message to log.
		"""
		print(("├── " if self.__indentation == 1 else
		       ("│" + "\t" * (self.__indentation - 1) + "└── " if self.__indentation > 1 else "\n")) + f"{message}")
