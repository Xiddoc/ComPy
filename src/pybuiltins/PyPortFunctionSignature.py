"""
Port a native function or object to Python.
"""
from typing import Optional, Iterable

from src.pybuiltins.PyPortSignature import PyPortSignature
from src.structures.TypeRenames import AnyFunction


class PyPortFunctionSignature(PyPortSignature):
	"""
	Port a native function or object to Python.
	"""

	function: AnyFunction
	code: str

	def __init__(self,
	             function: AnyFunction,
	             code: str,
	             dependencies: Optional[Iterable[str]] = None,
	             linked_ports: Optional[Iterable[str]] = None) -> None:
		self.function = function
		self.code = code
		self.dependencies: Optional[Iterable[str]] = dependencies
		self.linked_ports: Optional[Iterable[str]] = linked_ports
