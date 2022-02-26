"""
Port a native function or object to Python.
"""
from typing import Iterable, Optional


class PyPortSignature:
	"""
	Port a native object or object to Python.
	"""

	dependencies: Optional[Iterable[str]] = None
	linked_ports: Optional[Iterable[str]] = None

	def __init__(self,
	             dependencies: Optional[Iterable[str]] = None,
	             linked_ports: Optional[Iterable[str]] = None) -> None:
		# Set to fields
		self.dependencies: Optional[Iterable[str]] = dependencies
		self.linked_ports: Optional[Iterable[str]] = linked_ports
