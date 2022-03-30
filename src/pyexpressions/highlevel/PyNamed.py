"""
Python object which has it's own name.
"""
from abc import ABCMeta


class PyNamed(metaclass=ABCMeta):
    """
    Python object which has it's own name (identifier).

    For example, functions have a name which you can
    refer to them by. Variables and classes also follow
    this concept.
    """

    _name: str

    def get_name(self) -> str:
        """
        Returns the name of the object.
        """
        return self._name
