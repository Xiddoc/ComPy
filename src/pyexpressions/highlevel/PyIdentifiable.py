"""
Python object which has it's own name.
"""
from abc import ABCMeta

from src.pyexpressions.abstract.PyExpression import PyExpression


class PyIdentifiable(PyExpression, metaclass=ABCMeta):
    """
    Python object which has it's own name (identifier).

    For example, functions have a name which you can
    refer to them by. Variables and classes also follow
    this concept.
    """

    __id: str

    def set_id(self, new_id: str) -> None:
        """
        Update the name (ID) of the object.

        :param new_id: The new ID.
        """
        self.__id = new_id

    def get_id(self) -> str:
        """
        Returns the name of the object.
        """
        return self.__id
