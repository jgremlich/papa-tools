# Rollback command
import abc
from Command import AbstractCommand

class Rollback():

	def execute(self):
		print "Executing Rollback"


AbstractCommand.register(Rollback)