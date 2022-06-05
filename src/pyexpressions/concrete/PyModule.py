"""
Python module.
"""
from _ast import Module
from copy import deepcopy
from typing import List, Set

from src.pyexpressions.abstract.PyExpression import PyExpression
from src.pyexpressions.concrete.PyFunctionDef import PyFunctionDef
from src.pyexpressions.highlevel.PyScoped import PyScoped
from src.structures.Errors import ObjectAlreadyDefinedError


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
        # Update the debuggers, now that we have parsed the entire module
        self.get_logger().finalize_debuggers()

    def get_body(self) -> List[PyExpression]:
        """
        Gets all the body code of the current module.
        Useful for module imports.

        :return: The body (main) code of this module.
        """
        return self.__body

    def _transpile(self) -> str:
        """
        Transpiles the module to a native string.
        """
        from src.compiler.Constants import OUTPUT_CODE_TEMPLATE
        from src.pyexpressions.concrete.PyImport import PyImport

        # For each expression, we will compile them
        # However, we will separate this into "is a function"
        # or "is not", so that we can put all the function
        # definitions at the top of the output code.
        output_list: List[str] = []
        function_list: List[str] = []
        function_sigs: Set[str] = set()
        # Transpile each segment and add it to the output
        # Deep copy the body, since we don't want to alter it
        expr_index = 0
        body: List[PyExpression] = deepcopy(self.__body)
        while expr_index != len(body):
            # Get the current segment by index (as the body can dynamically expand, such as with PyImports)
            pyexpr = body[expr_index]

            # If the segment is a module import
            if isinstance(pyexpr, PyImport):
                # The native compiler will copy the imported module into the code directly
                # So we will do this for it instead, rather than create extra files
                # For each import (you can import multiple modules at the same time)
                for imported_module in pyexpr.get_imports():
                    # Insert into next index (inserting into current index will
                    # push the PyImport back into the loop, causing recursion)
                    insert_index = expr_index + 1
                    # Insert all of the code here
                    body[insert_index:insert_index] = imported_module.get_body()
            # If the segment is a function definition
            elif isinstance(pyexpr, PyFunctionDef):
                # Get the signature
                func_sig = pyexpr.transpile_header()
                # Check if it exists already
                if func_sig in function_sigs:
                    # Throw an error since you can't create the same function 2 times
                    raise ObjectAlreadyDefinedError(pyexpr.get_id())
                else:
                    # Add the signature to the list
                    function_sigs.add(func_sig)
                    # Add it to the function list
                    function_list.append(pyexpr.transpile())

            # Make sure it's not a dead expression
            elif not pyexpr.is_dead_expression():
                # Transpile and add to code segment
                # https://stackoverflow.com/q/9997895/11985743
                output_list.append(pyexpr.transpile() + ";")

            # Increment the index
            expr_index += 1

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
