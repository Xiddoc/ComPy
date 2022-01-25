"""
Port a native function or object to Python.
"""
from dataclasses import dataclass
from typing import Iterable, Optional

from src.structures.TypeRenames import AnyFunction


@dataclass
class PyPortFunctionSignature:
	"""
	Port a native function or object to Python.
	"""

	function: AnyFunction
	code: str
	dependencies: Optional[Iterable[str]] = None
