"""
Compiler class.
"""
from ast import AST, parse, unparse

from src.pyexpressions.concrete.PyModule import PyModule


class Compiler:
    """
    Compiler class to convert code to transpiled syntax trees.
    """

    @staticmethod
    def parse(source: str) -> PyModule:
        """
        Initiates the parsing sequence.
        This turns the code into a series of nodes, filled
        with the proper data structures alongside other nested nodes.

        :param source: The source code to compile.
        :return: A transpiled AST head node.
        """
        # Instantiate PyModule using AST
        return PyModule(parse(source))

    @classmethod
    def compile(cls, source: str) -> str:
        """
        Automatically parses the file, then transpiles it.
        This is essentially a wrapper function for parse().

        :param source: The source code to compile.
        :return: The transpiled source code.
        """
        return cls.parse(source).transpile()

    @staticmethod
    def unparse(expression: AST) -> str:
        """
        Takes an AST expression or node and unparses it back
        to Python code (or a Python expression, that is).

        :param expression: The AST node to unparse.
        :return: The Python representation of the node.
        """
        return unparse(expression)
