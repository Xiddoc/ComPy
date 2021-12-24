"""
Compiler class.
"""
from argparse import Namespace
from ast import Module, AST, parse

from src.DependencyManager import DependencyManager
from src.Output import Output
from src.VarHandler import VarHandler
from src.expressions.PyExpression import PyExpression


class Compiler:
	"""
	Compiler class to convert operations to ASM ops.
	"""

	__node: AST
	__args: Namespace
	__output: Output
	__var_handler: VarHandler
	__dependency_manager: DependencyManager

	def __init__(self, args: Namespace):
		# Use the given arguments
		self.__args = args

	def compile(self, source: str) -> None:
		"""
		Entry to compilation sequence.
		"""
		# Initialize an empty dictionary for variables
		self.__var_handler = VarHandler()
		# Initialize the dependency manager
		self.__dependency_manager = DependencyManager()
		# Initialize segment for code
		self.__init_output()
		# Parse the node into an abstract tree
		self.__node = parse(source, self.__args.file.name)

		# Walk down the node
		for node in self.__node.body:
			# Get the type of the node
			node_type = type(node)

			# Basic logger, remove later and add better UI
			print(f"Compiling expression {node}...")

			# Switch-like statement (if/elif) for matching node type
			# If multiline comment (Python literal string which is not assigned to a variable)
			if node_type == Module:
				# Do something later if necessary with imports
				continue
			else:
				# Evaluate the expression
				# Write it to the code segment
				self.__output.write(PyExpression.from_ast(node))

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

	def __init_output(self) -> None:
		"""
		Initialize the output dictionary structure.
		"""
		# Init output handler
		self.__output = Output()
		"""
		# Write defaults to sections
		self.__output.code("int main() {")
		self.__output.footer("return 0; }")
		# Implement builtins
		for func in self.__var_handler.get_funcs():
			# Write init of func
			self.__output.func(func.get_init())
			# Add dependencies
			self.__dependency_manager.add_dependencies(func.get_dependencies())
		"""
