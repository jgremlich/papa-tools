# Discard command
import abc
from Command import AbstractCommand

class Discard():

	def execute(self):
		print "Executing Discard"


AbstractCommand.register(Discard)