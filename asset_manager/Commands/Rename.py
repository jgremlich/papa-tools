# Rename command
import abc
from Command import AbstractCommand

class Rename():

	def execute(self):
		print "Executing Rename"


AbstractCommand.register(Rename)