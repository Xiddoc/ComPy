"""
Test comment.

Lots of escaped characters!
' " ` ; / % @ { } \
"""

# Assignment of type and value of constant or binary operation
a: int = (1 + 2) * 3

# Assignment of type and name with binary operation
b: int = a + 4

# Assignment of type and name
c: int = b

# Built-in function calls
print("The answer is... ")
print(c)


# Function declaration
def mul(x: int, y: int) -> int:
	"""
	Test function.
	"""
	return x * y


# Custom function usage
mul(1, 2)
mul(3, 4)
