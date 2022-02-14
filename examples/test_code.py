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

# Variables can be changed & built-in function calls
# noinspection PyUnresolvedReferences
c = inc(c)

# More built-in function calls
print("The answer is... " + str(c))


# Function declaration
def mul(x: int, y: int) -> int:
	"""
	Test function.
	"""
	# Calculate
	result: int = x * y
	# Uncomment to show that variables
	# can only be initialized once
	# result: int = 123
	return result


# Custom function usage
mul(1, 2)
mul(3, 4)
