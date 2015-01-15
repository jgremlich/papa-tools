# Abstract command class.
import abc

class AbstractCommand():
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def execute():
		"""Executes the command."""
		return