"""
Manager for C++ module dependencies.
"""


class DependencyManager:
	"""
	Manager for dependencies.
	"""

	__manager: set[str]

	def __init__(self):
		# Start manager
		self.clear_dependencies()

	def add_dependencies(self, dependencies: list[str]) -> None:
		"""
		Adds multiple dependencies to the manager.
		"""
		# For each depenency
		for dependency in dependencies:
			# Add it
			self.add_dependency(dependency)

	def add_dependency(self, dependency: str) -> None:
		"""
		Adds a dependency to the manager.
		"""
		self.__manager.add(dependency)

	def clear_dependencies(self) -> None:
		"""
		Clear all dependencies from the manager.
		"""
		self.__manager = set()

	def get_dependencies(self) -> set:
		"""
		Returns a set of all the dependencies.
		"""
		return self.__manager

	def format_dependencies(self) -> str:
		"""
		Returns a formatted list of all the include statements
		necessary for importing all the stored dependencies.
		"""
		return "\n".join(f"#include <{dependency}>" for dependency in self.get_dependencies())
