"""
Compiler class.
"""
from argparse import Namespace
from ast import AST, parse
from functools import reduce
from typing import Any

from src.Output import Output
from src.VarHandler import VarHandler
from src.pyexpressions.PyExpression import PyExpression


class Compiler:
	"""
	Compiler class to convert operations to ASM ops.
	"""

	__node: AST
	__args: Namespace
	__output: Output
	__var_handler: VarHandler

	def __init__(self, args: Namespace):
		# Use the given arguments
		self.__args = args

	def compile(self, source: str) -> None:
		"""
		Entry to compilation sequence.
		"""
		# Initialize an empty dictionary for variables
		self.__var_handler = VarHandler()
		# Init output handler
		self.__output = Output()
		# Parse the node into an abstract tree
		self.__node = parse(source, self.__args.file.name)

		# Walk down the node
		for node in self.__node.body:
			# Get the type of the node
			node_type = type(node)

			# Basic logger, remove later and add better UI
			print(f"Compiling expression {node}...")

			# Evaluate the expression
			# Write it to the code segment
			self.__output.write(PyExpression.from_ast_statically(node, None))

		# Complete by injecting headers
		# self.__output.header(self.__dependency_manager.format_dependencies())
		"""
		# Name (variable) usage
		elif node_type == Name:
			# Verify that name has been initialized
			# If it is not
			if not self.__var_handler.is_var_exists(node.id):
				# Raise an error
				raise VariableNotDefinedError(f"Variable '{node.id}' has was not initialized before usage.")
		
		elif expr_type == Name:
			# If the value is a name (variable)
			# Then return the variable name
			return Value(self.__var_handler.get_var(expression.id).var_name)
		elif expr_type == Call:
			# If value is an expression (function, literals)
			return Value(f"{expression.func.id}({','.join(self.eval_expr(arg).get_value() for arg in expression.args)})")
		"""

	def get_output(self) -> str:
		"""
		Returns the compiled output as a string.
		"""
		return self.__output.get_output()

	@staticmethod
	def get_attr(obj: AST, attribute_path: str) -> Any:
		"""
		A function that recursively traverses down an "attribute path"
		and retrieves the value at the end of the path.

		This function exists since the CPython ast library uses an odd
		system which dynamically adds attributes to the AST instances,
		instead of statically declaring them in their respective classes.

		Due to this, mypy will throw a type-checking error since it will
		not find these attributes in the class defenition. Hence, to work
		around this bug, we will use the getattr function to retrieve the
		attributes directly.

		@param obj: The AST object to traverse.
		@param attribute_path: The attribute path to use (for example, if passing
								the object 'expression', and you want to navigate
								to the 'target' attribute, then the 'id' attribute
								of the 'target' attribute, then for this parameter
								you would pass the string "target.id").
		"""
		# Split by .
		# For example: "expression.target.id" becomes ["expression", "target", "id"]
		attrs = attribute_path.split(".")

		# Built in functools' reduce function to cumulatively execute the getattr function
		# On the first 2 arguments of the list
		return reduce(getattr, attrs, obj)
