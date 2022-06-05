"""
Import statement.
"""
from _ast import Import
from importlib.util import find_spec
from typing import List

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyModule import PyModule
from src.structures.TypeRenames import GENERIC_PYEXPR_TYPE


class PyImport(PyExpression):
    """
    Import (and 'from' import) statement.
    """

    __imports: List[PyModule]

    def __init__(self, expression: Import, parent: GENERIC_PYEXPR_TYPE):
        super().__init__(expression, parent)

        # Initiate list
        self.__imports = []
        # For each name to import
        for module in expression.names:
            # Locate the module file
            with open(find_spec(module.name).origin, "r") as f:
                # Read the module and parse it
                from src.compiler.Compiler import Compiler
                self.__imports.append(Compiler.parse(f.read()))

    def get_imports(self) -> List[PyModule]:
        """
        Returns the list of modules imported in this single expression.
        Useful for baking imported modules directly into the output, rather
        than linking to the modules or transpiling them to extra files.

        :return: The list of PyModules imported.
        """
        return self.__imports

    def _transpile(self) -> str:
        """
        Transpiles the statement to a string.
        """
        # Transpile each module
        return "\n".join([module.transpile() for module in self.__imports])
