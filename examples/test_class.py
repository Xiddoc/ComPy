"""
Testing a class in Python.
"""


# noinspection PyMissingOrEmptyDocstring
class TestClass:
    """
    Class documentation.
    """

    test_field: int

    def __init__(self) -> None:
        # Initialize new temporary variable
        test_var: int = 1
        # Print it
        print(test_var)

    def increment_test(self) -> None:
        self.test_field += 1


# Initialize the class
test_instance: TestClass = TestClass()

# Get a public field
print(test_instance.test_field)
