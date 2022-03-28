"""
Python object which manages it's own private scope.
"""
from _ast import AST
from abc import ABCMeta
from typing import Optional

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.scopes.Scope import Scope
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyScoped(PyExpression, metaclass=ABCMeta):
    """
    Python object which manages it's own private scope.

    For example, functions have bodies in which
    variables retain there. They can be accessed
    from the external scope, but those initialized
    inside the function body cannot be used outside it.
    """

    __scope: Scope

    def __init__(self, expression: AST, parent: Optional[GENERIC_PYEXPR_TYPE]):
        # Super call
        super().__init__(expression, parent)

        # Create scope using exterior scope
        self.update_from_nearest_scope()

    def update_from_nearest_scope(self) -> None:
        """
        Overwrites this scope with the nearest scope available.
        """
        self.__scope = Scope(self.get_nearest_scope())

    # noinspection PyUnusedFunction
    def get_scope(self) -> Scope:
        """
        Returns our Scope instance.
        """
        return self.__scope
