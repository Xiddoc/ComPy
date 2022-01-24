"""
Test comment.

Lots of escaped characters!
' " ` ; / % @ { } \
"""

# # Importing a local file
# import examples.testimport
#
# # Incrementing variables from imported file
# examples.testimport.n += 1

# Assignment of type and value of constant or binary operation
a: int = (1 + 2) * 3

# Assignment of type and name with binary operation
b: int = a + 4

# Assignment of type and name
c: int = b

# Built-in function calls
print("The answer is... ")
print(c)

# Variables can be changed
c = 10


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
