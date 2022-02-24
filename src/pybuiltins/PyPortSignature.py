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
