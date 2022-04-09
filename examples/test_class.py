"""
Testing a class in Python.
"""


# noinspection PyMissingOrEmptyDocstring
class TestClass:

    test_field: int = 0

    def __init__(self) -> None:
        # Initialize new temporary variable
        test_var: int = 123
        print(test_var)

    def increment_test(self) -> None:
        self.test_field += 1


# Initialize the class
test_instance: TestClass = TestClass()

# Get a public field
print(test_instance.test_field)

# Execute a public method
test_instance.increment_test()

# The value changed!
print(test_instance.test_field)
