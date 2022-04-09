"""
Python module.
"""
from _ast import Module
from typing import List

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyFunctionDef import PyFunctionDef
from src.pyexpressions.highlevel.PyScoped import PyScoped


class PyModule(PyScoped):
    """
    Python module.
    """

    __body: List[PyExpression]

    def __init__(self, expression: Module):
        super().__init__(expression, None)
        # For each body expression
        # Create a PyExpression from the AST node
        self.__body = [self.from_ast(ast) for ast in expression.body]

    def _transpile(self) -> str:
        """
        Transpiles the module to a native string.
        """
        from src.compiler.Constants import OUTPUT_CODE_TEMPLATE

        # For each expression, we will compile them
        # However, we will separate this into "is a function"
        # or "is not", so that we can put all the function
        # definitions at the top of the output code.
        output_list: List[str] = []
        function_list: List[str] = []
        for pyexpr in self.__body:
            # Transpile each segment and add it to the output
            # If the segment is a function definition
            if isinstance(pyexpr, PyFunctionDef):
                # Add it to the function list
                function_list.append(pyexpr.transpile())
            elif not pyexpr.is_dead_expression():
                # Make sure it's not a dead expression
                # Transpile and add to code segment
                # https://stackoverflow.com/q/9997895/11985743
                output_list.append(pyexpr.transpile() + ";")

        # Format each part of the output,
        # then format each segment into the template string,
        # then return it all as a string.
        return OUTPUT_CODE_TEMPLATE.format(
            # For each dependency, insert the dependency as a string
            dependency_code="\n".join([f"#include <{dependency}>" for dependency in self.get_dependencies()]),

            # Inject native dependency headers
            ported_headers="\n".join([
                port.get_interface_function().transpile_header() + ";" for port in self.get_ported_dependencies()
            ]),

            # Inject native dependency bodies
            ported_code="\n".join([
                port.transpile() for port in self.get_ported_dependencies()
            ]),

            # Flatten the current code
            transpiled_funcs="\n".join(function_list),

            # Join the transpiled code
            transpiled_code="\n".join(output_list)
        )
