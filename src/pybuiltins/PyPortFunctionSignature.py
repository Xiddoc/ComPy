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

    # Mypy throws an error since it thinks we are overriding a method
    # func: AnyFunction
    code: str

    def __init__(self,
                 function: AnyFunction,
                 code: str,
                 dependencies: Optional[Iterable[str]] = None,
                 linked_ports: Optional[Iterable[str]] = None) -> None:
        # Call to super class constructor
        super().__init__(dependencies, linked_ports)
        # Set to fields
        self.func: AnyFunction = function
        self.code = code
