# Unlock command
import abc
from Command import AbstractCommand

class Unlock():

	def execute(self):
		print "Executing Unlock"


AbstractCommand.register(Unlock)