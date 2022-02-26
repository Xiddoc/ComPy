"""
Compiler class.
"""
from ast import AST, parse, unparse, Module

from src.compiler.Args import Args
from src.compiler.Util import Util
from src.pyexpressions.concrete.PyModule import PyModule


class Compiler:
    """
    Compiler class to convert operations to ASM ops.
    """

    __node: Module
    __pymodule: PyModule

    def parse(self, source: str) -> None:
        """
        Initiates the parsing sequence.
        This turns the code into a series of nodes, filled
        with the proper data structures alongside other nested nodes.
        """
        # Parse the node into an abstract tree
        # Cast node to proper type
        self.__node = parse(source, Args().get_args().file.name)

        # Initiate module
        self.__pymodule = PyModule(self.__node)

    def compile(self) -> str:
        """
        Returns the compiled output as a string.
        """
        return self.__pymodule.transpile()

    @staticmethod
    def unparse(expression: AST) -> str:
        """
        Takes an AST expression or node and unparses it back
        to Python code (or a Python expression, that is).

        :param expression: The AST node to unparse.
        :return: The Python representation of the node.
        """
        return unparse(expression)

    @classmethod
    def unparse_escaped(cls, expression: AST) -> str:
        """
        Takes an AST expression or node and unparses it back
        to Python code (or a Python expression, that is).
        Following that, it escapes all special characters
        so that it is now a printable literal where
        the special characters are not interpreted.

        :param expression: The AST node to unparse.
        :return: The *string-escaped* Python representation of the node.
        """
        # First, unparse the expression
        # Then, escape the string
        return Util.escape(cls.unparse(expression))
