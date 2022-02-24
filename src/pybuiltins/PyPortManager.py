"""
PyPortManager class.
Stores ported objects.
"""
from importlib import import_module
from typing import Dict

from src.compiler.Args import Args
from src.pybuiltins.PyPortFunction import PyPortFunction
from src.pybuiltins.PyPortFunctionSignature import PyPortFunctionSignature
from src.pybuiltins.builtins_port import ported_objs
from src.structures.Errors import InvalidArgumentError, ObjectNotDefinedError
from src.structures.Singleton import Singleton
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyPortManager(metaclass=Singleton):
	"""
	The PyPortManager class is a singleton class
	responsible for managing ported objects, loading them,
	and other such operations.
	"""

	# Static variable for ported library manager
	__linked_port_manager: Dict[str, PyPortFunctionSignature]

	def __init__(self) -> None:
		# Load the linked libraries (and builtins)
		self.__load_linked_libraries()

	def is_loaded(self, ported_name: str) -> bool:
		"""
		Checks if an object name is in the manager.

		:param ported_name: The name of the ported object.
		:return: True if it is linked, False if not.
		"""
		return ported_name in self.__linked_port_manager

	def call_port(self, ported_name: str, parent: GENERIC_PYEXPR_TYPE) -> PyPortFunction:
		"""
		Calls a ported object from the manager, instanciates it, and returns it.

		:param ported_name: The name of the ported object to call.
		:param parent: The parent expression to link the returned PyPortFunction to.
		:return: The created PyPortFunction instance which represents the requested port object.
		"""
		# Check if called port is linked
		if self.is_loaded(ported_name):
			# Compile the function to a PyPortFunction expression/object
			return PyPortFunction(self.__linked_port_manager[ported_name], parent)

		else:
			# Otherwise, throw an error
			raise ObjectNotDefinedError(ported_name)

	def __load_linked_libraries(self) -> None:
		"""
		Go through all the ported libraries that need to
		be linked, and load them into our static variable.
		"""
		# Start by defaulting to builtins
		self.__linked_port_manager = ported_objs
		# If any libraries were linked
		if Args().get_args().links:
			# Go through each passed parameter
			for port_library_path in Args().get_args().links.split(";"):
				# Catch errors (module can be non-existent, objects could be missing from file)
				try:
					# Import the linked library
					imported_module = import_module(port_library_path)

					# Try to get the ported objects
					obj_dict: Dict[str, PyPortFunctionSignature] = getattr(imported_module, "ported_objs")

					# Then add them to the ported object manager
					self.__linked_port_manager.update(obj_dict)
				except (AttributeError, ModuleNotFoundError):
					# The library is not valid or does not exist
					raise InvalidArgumentError(port_library_path)
